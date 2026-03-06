# Output Format Template

Use this exact structure when generating the development plan.

---

## 1. Escopos Identificados

### Escopo de Spikes Críticos Iniciais (se aplicável)

**Nome:** `[nome do escopo]`

**Descrição:** `[descrição detalhada dos spikes críticos iniciais]`

### Escopos Principais de Funcionalidade

1. **`[nome do escopo 1]`**: `[descrição]`
2. **`[nome do escopo 2]`**: `[descrição]`
3. **`[nome do escopo 3]`**: `[descrição]`
...

---

## 2. Sequência de Alto Nível dos Escopos Identificados

1. **`[nome do escopo]`**: `[justificativa da posição na sequência baseada na estrategia_sequenciamento]`
2. **`[nome do escopo]`**: `[justificativa da posição na sequência baseada na estrategia_sequenciamento]`
...

---

## 3. Sequência de Desenvolvimento Detalhada por Escopo

### Escopo: `[nome do escopo]`

**Objetivo geral do escopo:** `[descrição do objetivo principal deste escopo]`

**Definition of Done (DoD) do escopo (alto nível):** `[critérios de conclusão do escopo]`

**Sequência de tarefas detalhadas:**

#### 1. `[prefixo_se_necessario]` `💡 [sugestão]` `[nome da tarefa]`

**Objetivo/valor principal da tarefa:** `[descrição do que esta tarefa entrega]`

**Componentes chave envolvidos na tarefa:** `[lista de componentes, módulos ou sistemas]`

**Justificativa da sequência da tarefa:** `[explicação obrigatória usando os princípios 0-6. Se a posição desta tarefa for influenciada por um risco que você identificou 💡 [sugestão], deixe isso explícito aqui.]`

**Critérios de aceitação (alto nível) da tarefa:** `[lista de critérios]`

#### 2. `[prefixo_se_necessario]` `💡 [sugestão]` `[nome da tarefa]`

[... mesmo formato acima ...]

---

## 4. Resumo Final dos Nomes dos Escopos Principais de Funcionalidade Identificados

- `[nome do escopo 1]`
- `[nome do escopo 2]`
- `[nome do escopo 3]`
...

---

## Notes on Suggestions

When `modo_analise` is `sugestivo`, mark your contributions with `💡 [sugestão]`:
- Risks you identify that weren't explicitly marked
- Spikes you recommend
- Enabling tasks you suggest

When `modo_analise` is `estrito`, do not add any suggestions. Only work with explicitly provided information.
