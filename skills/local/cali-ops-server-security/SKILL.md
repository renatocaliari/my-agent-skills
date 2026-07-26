---
name: cali-ops-server-security
description: >
  [Cali] Server security audit and hardening for private servers behind Tailscale.
  Use when: auditing server security, hardening SSH/firewall/Docker, checking for
  vulnerabilities, setting up fail2ban, reviewing port exposure, responding to
  security alerts, or storing API tokens/secrets on the server.
  Covers 7 layers: CloudFlare, UFW, Tailscale, SSH, Docker, Application, Secrets.
  Triggers: "server security", "security audit", "harden server", "SSH hardening",
  "firewall rules", "UFW config", "fail2ban", "port security", "Docker security",
  "vulnerability check", "security review", "API token", "secrets storage",
  "~/.secrets", "env vars".

metadata:
  frequency: rare
  category: infra
  context-cost: low
disable-model-invocation: true
---

# Server Security Audit & Hardening

6-layer security model for private servers behind Tailscale.

## Security Layers

```
Internet → CloudFlare → UFW → Tailscale → SSH → Docker → App
```

| Layer | Purpose | Tool |
|---|---|---|
| 1. CloudFlare | CDN, DDoS, SSL, WAF, hide real IP | CloudFlare DNS + Tunnel |
| 2. UFW | Port filtering, default deny | UFW firewall |
| 3. Tailscale | WireGuard tunnel, private network | Tailscale |
| 4. SSH | Authentication, access control | OpenSSH / Tailscale SSH |
| 5. Docker | Container isolation, socket security | Docker Engine |
| 6. Application | Process isolation, env vars, volumes | Docker Compose |

## Required Stack

```bash
# Server packages
tailscale          # WireGuard tunnel
ufw                # Firewall
docker             # Container runtime
docker-compose     # Multi-container apps
fail2ban           # (optional) Brute-force protection

# SSH config
openssh-server     # SSH daemon
```

## Audit Commands

### Layer 2: UFW

```bash
sudo ufw status verbose
# Check:
#   Status: active
#   Default: deny (incoming), allow (outgoing)
#   Only tailscale0 ports allowed (22, 2222)
#   80/tcp and 443/tcp allowed (for web)
```

### Layer 3: Tailscale

```bash
tailscale status
# Check:
#   Server listed with correct IP
#   SSH enabled
#   Correct tags assigned

tailscale set --ssh=true  # ensure SSH enabled
```

### Layer 4: SSH

```bash
# Check critical settings
grep -E "PermitRootLogin|PasswordAuthentication|X11Forwarding|MaxAuthTries|LoginGraceTime" /etc/ssh/sshd_config

# Expected:
#   PermitRootLogin no
#   PasswordAuthentication no
#   X11Forwarding no
#   MaxAuthTries 3
#   LoginGraceTime 30

# Check deploy user
id deploy
cat /home/deploy/.ssh/authorized_keys
# Verify: command= restricts to docker compose only
# Verify: no-agent-forwarding, no-port-forwarding, no-X11-forwarding
```

### Layer 5: Docker

```bash
# Socket permissions
ls -la /var/run/docker.sock
# Expected: srw-rw---- root docker

# No insecure registries
cat /etc/docker/daemon.json | grep insecure
# Expected: nothing or empty

# Containers not exposing ports on 0.0.0.0
sudo ss -tlnp | grep -E "0\.0\.0\.0:(3001|3002|4040|9122|9111)"
# Expected: nothing
```

### Layer 6: Application

```bash
# Check container isolation
docker ps --format "{{.Names}}: {{.Ports}}"
# Expected: no 0.0.0.0 bindings for internal services

# Check volumes
docker inspect <container> | grep -A5 "Mounts"
# Expected: named volumes or specific host paths, not /
```

## Vulnerability Categories

### Critical (fix immediately)

| Issue | Risk | Fix |
|---|---|---|
| `PermitRootLogin yes` | Root SSH access | Set to `no` |
| `PasswordAuthentication yes` | Brute force risk | Set to `no` |

### Medium (fix soon)

| Issue | Risk | Fix |
|---|---|---|
| `X11Forwarding yes` | Display hijacking | Set to `no` |
| Processes on `0.0.0.0` | Port exposure | Bind to `127.0.0.1` or `tailscale0` |
| No fail2ban | No brute-force protection | Install + configure |

### Low (consider)

| Issue | Risk | Fix |
|---|---|---|
| No `AllowUsers` | Any user can SSH | Add `AllowUsers deploy` |
| No log monitoring | Missed intrusion attempts | Set up log alerts |

## Hardening Checklist

### SSH Hardening

```bash
# Add to /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
X11Forwarding no
MaxAuthTries 3
LoginGraceTime 30
AllowUsers deploy

# Restart SSH
sudo systemctl restart ssh
```

### UFW Hardening

```bash
# Verify rules
sudo ufw status numbered

# Remove any overly permissive rules
sudo ufw delete <rule-number>

# Rate limiting (optional)
sudo ufw limit 22/tcp
```

### Docker Hardening

```bash
# Restrict socket access
sudo chmod 660 /var/run/docker.sock
sudo chown root:docker /var/run/docker.sock

# No privileged containers
docker inspect <container> | grep Privileged
# Expected: false

# Read-only rootfs (optional)
docker run --read-only ...
```

### fail2ban (optional)

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban

# Configure
cat > /etc/fail2ban/jail.local << 'EOF'
[sshd]
enabled = true
port = 22,2222
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF

sudo systemctl restart fail2ban
```

## Examples

### Example 1: Full audit

```bash
# Run all checks
echo "=== UFW ===" && sudo ufw status verbose
echo "=== SSH ===" && grep -E "PermitRootLogin|PasswordAuthentication|X11Forwarding" /etc/ssh/sshd_config
echo "=== Tailscale ===" && tailscale status
echo "=== Docker ===" && docker ps --format "{{.Names}}: {{.Ports}}"
echo "=== Ports ===" && sudo ss -tlnp | grep -E "0\.0\.0\.0"
```

### Example 2: Fix critical vulnerabilities

```bash
# Fix SSH (run as root)
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config
sudo systemctl restart ssh
```

### Example 3: Check for exposed ports

```bash
# Find processes listening on 0.0.0.0
sudo ss -tlnp | grep "0\.0\.0\.0" | awk '{print $NF, $4}'
# Should only show: sshd (22), caddy (80,443)
```

## API Token Storage (3-Layer Model)

API tokens (Cloudflare, OpenAI, GitHub) must live outside the repo and outside `/etc/`. Convention: owner-only files under `~/.secrets/`, loaded by scripts via `source`. KISS, DRY, convention over configuration. Applies to any deploy user on any server.

### Three layers

| Layer | Lifetime | Location | Format | Example |
|-------|----------|----------|--------|---------|
| **L1 — runtime** | ephemeral | env vars injected into container | `KEY=value` | `docker run -e KEY=value ...` |
| **L2 — rest** | days/weeks | `~/.secrets/<service>.env` chmod 600 | `KEY=value` | `CF_API_TOKEN=...` |
| **L3 — provider** | rotating | Cloudflare/OpenAI/GitHub dashboard | n/a | TTL 24h, IP-restricted, scope-min |

**Defense in depth.** Each layer assumes the others may leak. Token in `.env` is IP-restricted (L3) so even if file leaks, attacker needs same IP. TTL short (L3) so leaks expire fast.

### Setup

```bash
mkdir -p ~/.secrets && chmod 700 ~/.secrets
$EDITOR ~/.secrets/cloudflare.env   # one file per service
chmod 600 ~/.secrets/*
```

Each file follows `KEY=value` convention. One token per file. Naming: `<service>.env` (`cloudflare.env`, `openai.env`, `github.env`). `README.md` in `~/.secrets/` lists which services have keys and rotation dates.

### Reading tokens from scripts

```bash
set -a; source ~/.secrets/cloudflare.env; set +a
curl -H "Authorization: Bearer $CF_API_TOKEN" ...
```

Pattern: `set -a` auto-exports, `source` reads, `set +a` stops. Works in any bash script.

### Why not Vault / SOPS / Doppler for 1 server

| Tool | When it pays off | When it's overhead |
|------|-----------------|---------------------|
| **`.env` chmod 600 (this)** | 1 server, <20 secrets, 1-2 deploy users | — |
| SOPS + age | secrets committed to git in CI | single-server manual ops |
| HashiCorp Vault | 10+ services, compliance (SOC2/PCI), dynamic secrets | single personal server |
| Doppler / Infisical | multi-team, audit/RBAC needed | single user, single server |
| 1Password CLI | team vault + dev local | CI performance, single-server automation |
| dotenvx | encrypted-at-rest in git, KMS-managed | single private server already encrypted at disk |

**Migration trigger:** move to Vault or Doppler when you hit 3+ servers OR 50+ secrets OR need audit log OR compliance requirement.

### Audit (run periodically)

```bash
# Check no secrets leaked to world
ls -la ~/.secrets/                              # expect drwx------, -rw------
ls -la ~/.secrets/*.env                         # expect -rw-------, owned by deploy

# Check no secrets in shell history
history | grep -iE "api[_-]?key|token=|secret=" | head
# If found: unset HISTFILE, rotate token, re-save via editor

# Check no secrets in env vars dump (L1 layer leakage)
env | grep -iE "api[_-]?key|token|secret" | head
# Expected: nothing or short-lived vars only

# Check no secrets in git (if you have a repo)
git -C ~/mercury-docker log -p | grep -iE "api[_-]?key|token=|secret=" | head
```

### Test Cases (should)

- [ ] `~/.secrets/` exists, mode 700, owned by deploy
- [ ] All `*.env` files in `~/.secrets/` are mode 600, owned by deploy
- [ ] Scripts use `source ~/.secrets/<service>.env` (not hardcoded tokens)
- [ ] Each provider token has IP restriction + TTL + minimal scope
- [ ] No tokens in `~/.bash_history`, `~/.viminfo`, or git history
- [ ] At least one README.md in `~/.secrets/` lists services + rotation dates

### Should NOT

- Tokens in `docker-compose.yml` committed to git
- Tokens in `/etc/` with world-readable permissions
- Tokens in shell history (use `set +o history` before pasting, or editor)
- Long-lived tokens (>30 days TTL) without rotation schedule
- Tokens with broader scope than the task needs

## Edge Cases

### Server is public (no Tailscale)
- UFW must allow SSH on standard port (22) from specific IPs
- Consider fail2ban for brute-force protection
- Use key-based auth only (no passwords)

### Multiple deploy users
- Each user needs separate `command=` in authorized_keys
- Use `AllowUsers` to whitelist all deploy users
- Verify each user's Docker group membership

### Root access needed temporarily
- Use `sudo` from deploy user instead of PermitRootLogin
- Add deploy user to sudoers: `deploy ALL=(ALL) NOPASSWD: /usr/bin/docker`
- Never leave PermitRootLogin yes permanently

### Container exposes ports
- Check `docker-compose.yml` for `ports:` section
- Bind to `127.0.0.1:host_port` instead of `host_port:host_port`
- Use UFW to block if needed

## Test Cases

### Should

- [ ] UFW active with default deny incoming
- [ ] SSH only accessible via Tailscale (port 22, 2222)
- [ ] PermitRootLogin set to no
- [ ] PasswordAuthentication set to no
- [ ] Deploy user is non-root with docker group
- [ ] Deploy SSH key has command= restriction
- [ ] Docker socket owned by root:docker
- [ ] No processes listening on 0.0.0.0 for internal services

### Should NOT

- [ ] Root should NOT be able to SSH directly
- [ ] Password auth should NOT be enabled
- [ ] Internal services should NOT bind to 0.0.0.0
- [ ] Deploy user should NOT have shell access
- [ ] Docker socket should NOT be world-readable
