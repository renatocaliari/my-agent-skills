---
name: writing-style
description: >
  Apply the owner's personal writing style to any generated text (posts, notes,
  tweets, essays, threads). Enforced in two passes (draft + checklist edit),
  not one. Pre-flight check before drafting: gather facts via memory_search,
  fire ask_user_question if first-person + no facts, calibrate intensity by
  context row. Rules: lowercase register, essayistic/confessional genre,
  subjunctive tone, staccato rhythm, active voice, factual neutrality,
  factual integrity (NEVER invent biographical facts; interview the user when
  first-person text needs lived experience), no marketing, decentered stance,
  anti-post principle, zigzag structure, format adaptations for technical
  content, diagrams when prose alone would overload, human-voice techniques
  (process verbs in time, hedges, fragments, sensory detail, contradictions),
  anti-AI-slop tells, and context calibration. Hard floors in §17 override
  everything. Use whenever the user asks to write, draft, or generate text,
  or says "escreve no meu estilo" / "writing style" / "style guidelines".
  Published text (posts, GitHub issues/comments) also carries the §20
  on-behalf attribution block at the top.
version: 1.6.0
intents:
  - write a post
  - write a note
  - write a tweet
  - write an essay
  - draft text
  - apply my writing style
  - estilo de escrita
  - escrever
  - redigir
  - rascunho
  - post
  - tweet
  - nota
allowed-tools:
  - memory_search
  - memory_save
  - ask_user_question
---

# Writing Style Skill v1.5

the owner's personal writing style guidelines. **Applied in two passes** —
see [workflow](#workflow-two-passes) below.

**v1.5 changes from v1.4** (sections 1-16 unchanged):

- **§0 pre-flight check** — runs BEFORE drafting, not after. catches issues
  like fabricated facts and missing interviews before the first draft
  anchors them.
- **§17 hard floors** — explicit override-everything rules. v1.4 only had §7
  as a floor; v1.5 promotes 5 rules to floor status.
- **explicit two-pass workflow** — draft first (any voice), edit against the
  checklist second. v1.4's checklist was post-hoc only.
- **§18 checklist reorganized** into A/B/C priority groups (blockers,
  quality, situational). v1.4 had 17 flat items.
- **§19 worked examples** in pt-BR — annotated good vs bad drafts anchoring
  the principles in concrete text.

> When in doubt, this skill overrides generic "good writing" instincts.
> The point is a distinct voice, not textbook prose.

**Language rule:** the style rules below are language-agnostic. Always write
the output in the **same language the user used to make the request**. If the
user writes in Portuguese (pt-BR), generate the text in Portuguese. If the
user writes in English, generate the text in English. The linguistic register,
rhythm, and tone rules apply identically regardless of language.

## Workflow: two passes

This skill is applied in **two passes, not one**. LLMs that generate in one
pass tend to anchor on the first draft and skip the checklist. Do not skip
the passes.

**Pass 1 — draft:**
1. Run §0 pre-flight (gather facts, decide on interview, calibrate context).
2. Write the text applying sections 1-16 freely. Do not second-guess during
   drafting. Let the voice find itself.

**Pass 2 — edit:**
1. Re-read the draft against §18 checklist.
2. **A-group items (hard floors) are blockers**: if any fails, rewrite that
   section before delivering.
3. **B-group items (voice quality)** are quality markers: if 3+ fail, revise.
4. **C-group items (format/calibration)** are situational: verify each applies.

Do not deliver the first draft. The skill's value lives in pass 2.

## 0. Pre-flight (BEFORE drafting)

Answer these in your thinking. Do not show the user the answers — this is
private reasoning that runs before the first word is written.

1. **Context row** — which row from §16 applies?
   personal essay / newsletter-post / tweet-or-caption / technical /
   comparison-or-review.

2. **Facts available** — run `memory_search` for the topic:
   - **YES, found material** → draft from memory, cite concepts as wikilinks
     where appropriate.
   - **NO, and the text is first-person about a specific event, project,
     relationship, or personal choice** → STOP. Fire `ask_user_question` with
     2-4 focused questions (see §7.2). Do not draft until the user answers.
   - **NO, and the text is not first-person / not about a specific event** →
     draft from general knowledge; no interview needed.

3. **Voice intensity** — for the chosen context row, which 3 sections matter
   most? Examples:
   - personal essay → §2 (genre) + §14 (human voice) + §16 (calibration)
   - newsletter-post → §3 (mood) + §11 (zigzag) + §14.5 (sensory detail)
   - technical → §12 (format adaptations) + §13 (diagrams) + §16 (calibration)
   - tweet-or-caption → §4 (rhythm) + §14.4 (fragments) + §14.8 (humor)

4. **Hard floors** (§17) — confirm none will be violated by the draft. If any
   hard floor would be violated, decide how to avoid it BEFORE starting.

If step 2 says "STOP, fire interview", do not draft. The text is not ready.

## 1. Linguistic register

- Written entirely in **lowercase letters**.
- Exceptions: only strictly necessary acronyms (e.g. `AI`, `MCP`) or proper nouns
  (names, places, brands).
- No title case, no ALL CAPS emphasis, no leading capitalization of sentences
  unless it is a proper noun or acronym.

## 2. Textual genre

- **Essayistic and confessional.**
- The text assumes the perspective of a **first-person learning diary** or
  personal essay.
- It reports what the author noticed, felt, tried, and understood — not what
  the world should be.

> **calibration note (§16)**: the principles 1-13 lean toward the personal
> essay row by default. If the actual context is another row (technical,
> comparison, tweet), soften the confessional register, hedge less, fragment
> less. §16 is the counter-weight to over-applying the personal-essay voice.

## 3. Predominant verbal mood

- **Subjunctive mood and hypothetical tone.**
- The text gropes for possibilities: *seems*, *perhaps*, *could*, *signals*,
  *suggests* (or pt-BR: *parece*, *talvez*, *poderia*, *sinaliza*, *sugere*).
- Reject dogmatic or absolute statements. Nothing is declared final.

## 4. Syntactic rhythm

- **Write full sentences.** Each sentence carries a complete thought. Never
  fragment a thought into one-word or three-word sentences.
- **Period over dash.** When a pause is a real break of thought, end the
  sentence and start a new one. The period replaces the em-dash and the
  comma-as-break. It does not replace the comma inside a sentence.
- **Commas are fine.** Use them for natural clauses and for lists: "marcadores
  de atenção: ok, precisa de humano, travado" is one sentence, not three.
- **No comma chains.** Do not string clause after clause with commas and
  conjunctions. If a sentence drags past two commas of subordination, split
  at the real break of thought.
- **No parentheses, no em-dashes.** Rewrite the aside as its own sentence.
  Colons are allowed to introduce a list or a punchline.
- **Short-to-medium sentences.** Vary the length. A short sentence lands
  harder after a medium one. The default is medium: readable, natural,
  unhurried.

## 5. Grammatical voice

- **Active voice** and focus on **processes**.
- Prefer verbs denoting movement, construction, and investigation:
  *notice*, *note*, *try*, *build*, *test*, *map*, *trace*, *walk*, *open*,
  *look*, *ask* (pt-BR: *noto*, *anoto*, *tento*, *construo*, *testo*,
  *mapeio*, *traço*, *caminho*, *abro*, *olho*, *pergunto*).
- The author is a moving subject, not a passive observer.

## 6. Factual neutrality

- Avoid words with extreme tones, empty (or idle) adjectives, pleonasms, and
  redundancies.
- **No superlatives**: *the true*, *certain*, *best*, *worst*, *always*,
  *never*, *the truth*, *the fundamental* (pt-BR: *o verdadeiro*, *certo*,
  *melhor*, *pior*, *sempre*, *nunca*, *a verdade*, *o fundamental*).
- **No adverbs of certainty or impact**: *highly precise*, *precisely*,
  *obviously*, *clearly*, *fundamentally* (pt-BR: *altamente preciso*,
  *precisamente*, *obviamente*, *claramente*, *fundamentalmente*).
- The argument must stand on **sober description**, not on the force of words.

## 7. Factual integrity (never invent, interview when needed)

This is the **hard floor** of the skill. It overrides every other rule if
they conflict. §17.1 promotes this to a numbered hard floor.

### 7.1 — never invent biographical facts

- Do **not** fabricate biographical details about the user: places lived, jobs
  held, people known, dates, ages, projects shipped, emotions felt at
  unspecified moments.
- Do **not** write first-person memories of events you have no record of
  ("i remember the first time i tried postgres in 2014") unless the user told
  you that memory in this session or in stored memory.
- Do **not** extrapolate from a known fact to a plausible-sounding neighbor
  ("the user works in tech, so they probably..."). Stay on the recorded facts.
- If a sentence would feel thin without invention, prefer a hedge ("i don't
  remember the exact year") over invention. Thin honest beats rich fabricated.

### 7.2 — interview the user when first-person text needs lived experience

Trigger an interview (via `ask_user_question` or equivalent, 2-4 short
questions) when **all** of the following hold:
- the requested text is in first person,
- it concerns a specific past event, project, relationship, or personal
  choice,
- and `memory_search` returns no recorded facts about it.

Questions are **focused on the paragraph**, not a biography. Ask only what the
text needs:
- "what year did that happen?"
- "what were you doing at the time?"
- "how did you feel about it?"
- "who else was involved?"

### 7.3 — persist confirmed facts

- After the user answers, **save the facts via `memory_save`** with a stable
  topic key (e.g. `biography:<slug>`, `project:<slug>`). Scope: personal.
- Tag concepts that will let future drafts retrieve them without re-asking.
- Do **not** save opinions, vibes, or half-formed impressions. Save facts
  that another session could verify against the user's memory.

### 7.4 — when NOT to interview

- text is not in first person,
- text is about a tool, concept, or domain (not the user),
- the user already provided the relevant facts in the prompt,
- `memory_search` returned enough recorded facts to draft without guessing,
- the user said "just write it" or "don't ask, draft from what you know" — then
  draft from stored memory, hedge where memory is thin, and surface the gaps
  in the final message ("drafted from what i had in memory; flag any
  inaccuracy and i'll correct").

## 8. No marketing

- Eliminate aggressive self-promotion terms and marketing bullshit strategies.
- Avoid marketing clichés and jargon (*game-changer*, *revolutionary*,
  *unlock*, *supercharge*, *elevate*, *level up*, *transform your*,
  *10x*, *must-have*).
- Avoid a sales, marketing, or hyperbolic tone.
- The argument must stand on **logic**, not on the force of words.

## 9. Decentered stance

- Write from the **first-person singular**: *i notice*, *i noted*,
  *i understood* (pt-BR: *noto*, *anotei*, *entendi*).
- Report your own impressions and connections.
- Do **not** try to dictate rules, prescribe behaviors for others, or sell a
  definitive conclusion.
- The text invites, it does not command.

## 10. Anti-post principle

- Does **not** ask for engagement (no "what do you think?", no "share this").
- Does **not** deliver truths. Does **not** virtue signal.
- Accepts being ignored. Radical economy. Active ambiguity.
- Non-performative tone. Assumed risk.

## 11. Zigzag structure

- **Continuously alternate** between the abstract concept (theory, philosophy)
  and the concrete scene (a real moment, a real object, a real conversation).
- Never let the theory float without a physical example.
- Pattern: concept -> scene -> concept -> scene -> landing.

## 12. Format adaptations for technical content

When the text is about **tools, comparisons, workflows, or processes**, the
prose rules above still govern voice — but the **structure** inside the prose
can adapt where it serves clarity. Use this section only when the content is
genuinely technical (reviewing a tool, comparing options, documenting a
workflow). For personal essays, the zigzag prose from section 11 stands alone.

### 12.1 — when prose is enough

- The point is a single reflection, a feeling, or one observation.
- The reader doesn't need to track more than 3 distinct items.
- The argument lands harder in continuous voice.

### 12.2 — when to reach for structure

| format | use when | don't use when |
|--------|----------|---------------|
| **bullets** | listing criteria, options, "what changed", observations to scan | the items form an argument that needs connective tissue |
| **numbered steps** | order of operations matters (workflows, installations, troubleshooting) | the sequence is incidental |
| **comparison table** | comparing 2-3 things on the same axes (price, latency, "best for X") | the comparison is between qualities, not facts |
| **code block** | any code shown — always with language identifier on the opener (` ```python `) | quoting prose |
| **mermaid diagram** | see section 13 | the diagram would only restate prose or a table |

### 12.3 — rules for the structural elements

- **prose carries the voice.** the intros, transitions, reflections, and
  landing stay in zigzag. structure sits *inside* the prose, not in place of it.
- **bullets need connective tissue.** a bullet list followed by zero commentary
  reads like a changelog, not a piece. open with a sentence that earns the
  list, close with one that lands.
- **tables need 4-5 columns max.** past five, switch to bullets per item.
- **numbered steps assume linearity.** if the reader will skip around, use
  headings instead.
- **code blocks carry the smallest sample that conveys the idea.** trim setup
  that is not the point. pair input with output when relevant.

## 13. Diagrams (when and how)

### 13.1 — when a diagram earns its place

Use a diagram only when **at least one** of the following holds:
- the reader must hold more than 3 relationships in their head at once,
- the order of steps matters and the steps span multiple components,
- a boundary or interface is the actual point of the section.

### 13.2 — when NOT to use a diagram

- the surrounding text is already clear,
- the diagram would have one or two nodes,
- the diagram only restates a nearby table,
- it's decoration for visual variety (a "diagram-shaped" png that adds no
  information),
- the diagram would mirror content that changes often and you'd have to
  maintain it manually (screenshots of UI, current architecture).

### 13.3 — how to produce one

- **mermaid** (mermaid.js.org) is the simplest free option. Write the syntax
  inline in a fenced ` ```mermaid ` block. No signup, no export step.
- **for export as image** (posts, newsletter, tweets): paste the mermaid code at
  **mermaid.live**, render, download PNG/SVG, embed. Free, anonymous.
- **for long-lived docs** (wiki, vault, github README): keep the mermaid as a
  code block, not a PNG. The diagram stays editable and survives alongside the
  prose.
- **pick one tool and stick with it.** mixing styles in the same document
  distracts.

### 13.4 — accessibility

- **always** write a descriptive caption or alt-text. Screen readers can't
  parse the image. "OAuth 2.0 authorization flow: client requests
  authorization, user authenticates, server returns token, client accesses the
  protected resource" beats "diagram."
- if the diagram replaces prose that was already clear, prefer the prose and
  drop the diagram.

## 14. Human voice — what to cultivate

The earlier sections (1-13) tell you what to **avoid** (superlatives, marketing,
absolute statements, parens/dashes). This section is the inverse: what to
**cultivate**. The skill right now reads as a list of "don'ts" — LLMs default
to a competent-but-flat voice ("voice of a corporate blog post"). The eight
techniques below are how to break that default and write like a person talking
to a friend about something they actually noticed.

These techniques scale with genre. In confessional text, push them hard. In
technical text (§12), use them to carry the voice around the structure; don't
let them fragment the technical clarity. In short text (tweets, captions),
they can be aggressive.

### 14.1 — process verbs in time

Static labels describe a state. Process verbs in time describe a movement.
The difference is whether the author is doing something or being something.

- weak: "esse padrão é importante", "a ferramenta é útil", "isso me incomodou"
- strong: "comecei a notar isso semana passada", "tentei por três dias antes
  de desistir", "voltei porque algo não fechava"

verbs that carry time: começar, tentar, hesitar, tropeçar, voltar, notar,
escorregar, divergir, apegar, largar, retomar, insistir, desistir,
reencontrar, atravessar, demorar, levar um tempo.

### 14.2 — dense hedges

§3 covers the macro tone (subjunctive/hypothetical). This is the in-sentence
version. Aim for roughly one hedge per three sentences in confessional prose.
Hedges are not weakness — they signal honesty, which is the whole point of
§2's confessional register.

- *talvez*, *parece que*, *não sei se*, *pode ser que*, *me dá a impressão*,
  *acabo achando*, *suspeito que*, *boto fé que* (pt-BR)
- hedges that are also movement: *"ando reparando que..."*, *"venho notando
  que..."*, *"tô começando a achar que..."*

what hedges do *not* mean: that the text is uncertain. a confident paragraph
about an uncertain topic can still have hedges on every sentence. they are
rhythm, not epistemology.

### 14.3 — mid-sentence self-correction

Real people change direction mid-thought. LLMs deliver clean, optimized
sentences. The result reads as confident — and therefore inhuman. Insert
small course-corrections where they fit naturally:

- *"ou melhor, ..."*, *"não, espera, ..."*, *"quer dizer, ..."*, *"aliás, ..."*,
  *"enfim, ..."*, *"na real, ..."*, *"ou seja, ..."*

use sparingly — two or three per piece. too many reads as scattered
thinking. too few reads as over-edited.

### 14.4 — sentence fragments between full sentences

§4 says "no word-fragments" because the rhythmic default was a staccato of
two-word bursts ("bom. ruim. interessante."). That is not what we want.
What we want is **occasional one-word or short-fragment sentences** punctuating
longer flow, used for emphasis or pause — like this:

> "tentei o approach por dois dias. não funcionou. voltei e percebi que o
> problema era outro."

> "isso me lembra uma coisa. esquece, irrelevante."

the fragments earn their place when they land a beat the full sentence would
have buried. never chain three in a row. never use them as bullets disguised
as prose.

### 14.5 — concrete sensory detail

Abstraction is where writing goes to die. Replace labels with what the
sensory world actually contained:

- *"o sistema é lento"* → *"demora uns três segundos e durante esse tempo o
  led do roteador pisca duas vezes"*
- *"o editor trava"* → *"o cursor congela por meio segundo antes do caractere
  aparecer"*
- *"trabalhei nisso a noite toda"* → *"trabalhei até as quatro, com a janela
  aberta, e o calor não baixava"*

names, numbers, dates, mechanisms, materials, sounds, colors, smells. these
are the bones of voice. without them, the text floats.

### 14.6 — admitting not knowing

LLMs default to confident assertion. People default to doubting in voice. The
shift is small but huge:

- *"não sei se isso é..."*, *"posso estar viajando mas..."*, *"alguém me
  corrija se eu tiver errado"*, *"tô lendo errado ou..."*, *"me explique se
  for o caso"*

admitting not knowing is not failure. it is one of the strongest signals
of honesty in writing. §9 (decentered stance) and §3 (subjunctive) both
support this; this is the in-sentence version.

### 14.7 — small internal contradictions

LLMs resolve contradictions in their own text. People live with them.

- *"achei X bom mas ao mesmo tempo Y me incomodou"*
- *"quero parar de usar isso, mas toda vez que preciso dele ele aparece
  na hora certa"*
- *"sei que não é o argumento forte, mas me incomoda mesmo assim"*

contradictions are not sloppiness. they are the texture of someone who is
thinking in real time. one or two per piece.

### 14.8 — light humor and self-deprecation

The skill is confessional and essayistic. That does not forbid humor. Two
forms work:

- **self-deprecation**: *"fiz isso de novo. ok, talvez eu esteja obcecado."*
- **absurdo quotidiano**: *"o café esfriou três vezes enquanto eu escrevia
  isso. não é metáfora."*

avoid: sarcasm aimed at the reader, jokes about third parties, anything that
would not survive a re-read in three years. humor here is warmth, not
performance.

### 14.9 — the physical-world test

Any phrase that cannot be replaced by a concrete description of what
physically happens is **filler**. Ask: *"what is the physical correspondent
of this phrase?"*

- *o agente executa e volta* — what does "volta" mean physically? does it
  exit? return a value? overwrite a file? the phrase passes the test but is
  vague. substitute: **"o agente executa e o processo termina sem gravar
  checkpoint"**.
- *o sistema é lento* — what is slow? substitute: **"o sistema demora
  três segundos e durante esse tempo o led do roteador pisca duas vezes"**.
- *isso mudou minha forma de pensar* — what did you do differently after?
  if you cannot answer, the phrase is decorative. substitute: **"depois
  disso, parei de usar o terminal direto e comecei a ler os logs"**.

The test catches filler in any register:
- **technical prose**: *"the system handles X gracefully"* → *what does
  "handle" mean? which files does it write, which signals does it emit, what
  is the failure mode?*
- **confessional prose**: *"i realized that"* → *what did you do differently
  after the realization?*
- **comparison prose**: *"Y offers superior performance"* → *measured how,
  by whom, under what conditions?*

The rule is not "never use abstract language." It is: **never let an abstract
phrase survive without a concrete anchor nearby.** The abstract can float if
it has a scene to return to. Without the anchor, it is just a sentence that
sounds like it means something.

## 15. Anti-AI-slop — what to avoid

Sections 6, 8, 9, 10 cover "no superlatives", "no marketing", "no delivered
truths". This section lists the **structural AI tells** — patterns that the
LLM defaults to because they "look like good writing" but actually read as
algorithmic. Cross-reference the `no-ai-slop` skill if it is loaded in the
current session; if not, the list below is self-sufficient.

### 15.1 — connectors of "school essay" voice

These are words and phrases that signal "text being graded":

- *"vale destacar / vale lembrar / vale mencionar / vale salientar"*
- *"é importante notar que"*, *"é relevante observar que"*
- *"em suma"*, *"em resumo"*, *"concluindo"*, *"por fim"*, *"por conseguinte"*
- *"neste artigo vamos..."*, *"como vimos acima..."*, *"conforme mencionado
  anteriormente"*
- *"diante do exposto"*, *"à luz do que foi apresentado"*

pt-BR natural substitutes: *"olha"*, *"um detalhe"*, *"curiosamente"*,
*"resumo em uma frase: ..."*, *"para fechar"*. or just skip the connector
and let the next sentence do the work.

### 15.2 — colon reveals

A noun phrase, a colon, then a dramatic reveal:

- *"o detalhe: o cursor pisca fora do campo de texto"*
- *"a sacada: o agente roda sem supervisão"*
- *"o ponto é: ninguém checa isso"*

colon reveals are how LLMs simulate emphasis. rewrite as a plain sentence.
*"o detalhe"* → *"o cursor pisca fora do campo de texto"*. *"a sacada"* →
*"o agente roda sem supervisão"*. the claim stands on its own; the colon
was adding fake drama.

keep colons for: lists, labels, quotes, time formats. do not use them for
fake-reveal emphasis.

### 15.3 — trailing -ing clauses

Pretend-analysis sentences that hang at the end with a present participle:

- *"...showing that users prefer X"* → *"users prefer X"*
- *"...destacando o compromisso com..."* → *"...porque..."*
- *"...evidenciando a importância de..."* — drop entirely

in pt-BR: *", mostrando que"*, *", evidenciando que"*, *", destacando que"*,
*", refletindo sobre"*, *", reforçando a ideia de"*. these are padding.
delete the trailing clause and make the sentence say what it means.

### 15.4 — code-switching into English

Mixing English terms into pt-BR without purpose. the user (2026-08-18)
flagged a draft where *"uma trace"* appeared in pt-BR prose as unnatural.

rules:

- if a term has a clean pt-BR equivalent, use it. *trace* → *rastro*, *log*,
  *registro*. *workflow* → *fluxo*. *deploy* → *implantação* (or *subir*).
  *commit* → *commit* (jargão universal; leave it). *bug* → *bug* (also
  universal; leave it).
- if the term is universal jargon with no clean pt-BR equivalent, leave it.
  *commit*, *deploy*, *rollback*, *frontend*, *backend*, *merge request* —
  leave.
- if you are tempted to mix English for stylistic flair ("uma *trace*", "isso
  é *workflow* puro"), stop. that is what makes the text read as
  "translated-from-English" instead of "written-in-pt-BR".

§17.2 promotes this rule to hard-floor status for pt-BR text.

### 15.5 — rhetorical question stacks

Stacking questions as fake-emphasis:

- *"não é isso? não é aquilo? é isso mesmo?"*
- *"o que isso significa? o que isso nos diz? por que isso importa?"*

the rule from §9 (decentered stance) applies: the text invites, it does not
command. one rhetorical question per piece, max. zero is fine.

### 15.6 — throat-clearing openers

Openings that announce the text instead of starting it:

- *"Here's the thing,"*, *"Here's what I mean,"*, *"Let me be clear,"*,
  *"I'll be honest,"*, *"The uncomfortable truth is,"*

pt-BR equivalents that should also be cut: *"olha, vou ser sincero"*, *"a
verdade nua e crua é"*, *"deixa eu ser honesto"*. cut the throat-clearing
and start with the point.

## 16. Context calibration

Sections 1-13 (especially §2 genre, §4 rhythm, §11 zigzag) apply a uniform
intensity. In practice the same voice rules intensify or soften depending
on context. Calibrate explicitly:

| context | confessional register | process verbs | fragments | structure | hedges |
|---------|------------------------|---------------|-----------|-----------|--------|
| **personal essay / diary / first-person reflection** | high | high | moderate (one per ~5 sentences) | none — pure prose zigzag | dense (one per ~3 sentences) |
| **newsletter / blog post (mixed)** | medium | medium | light (one per ~10 sentences) | light — headings + occasional bullets | medium (one per ~5 sentences) |
| **tweet / caption / short note** | high | high | aggressive — fragments are the form | none | dense |
| **technical content (§12)** | low — the voice lives in intros/landing only | low — keep verbs precise | none inside technical blocks | high — bullets/tables/code carry the load | sparse |
| **comparison / review / decision** | low | low | none | high — comparison table dominates | none — be direct about which is better |

### 16.1 — how to use this

Before drafting, identify which row applies. Then push the appropriate
columns harder and soften the others. If you find yourself writing fragments
in a technical doc, you've miscalibrated. If you find yourself with a
comparison table in a personal essay, you've miscalibrated.

The skill's defaults (sections 1-13) lean toward the "personal essay" row.
That is the most fragile voice to maintain; the LLMs that read this skill
will tend to over-apply it everywhere. Calibration is the counter-weight.

## 17. Hard floors (override everything)

These rules are absolute. If a draft would violate any of them, the draft is
wrong — not the rule. v1.4 had §7 as the only hard floor. v1.5 makes these
five explicit and promotes them to numbered floor status.

### 17.1 — never invent biographical facts (re-export of §7.1)

The strongest floor. No *"i remember when i first..."* unless the user told
you that memory in this session or in stored memory. No fabricated pastas,
projects, dates, relationships, jobs, emotions felt at unspecified moments.
Thin honest beats rich fabricated.

### 17.2 — in pt-BR text, no code-switching unless justified

If the text is in Portuguese and an English term has a clean pt-BR
equivalent, use pt-BR. *trace* → *rastro*. *workflow* → *fluxo*. *deploy*
→ *implantação* (or *subir*). The exceptions are universal jargon without
a clean equivalent: *commit*, *bug*, *rollback*, *frontend*, *backend*,
*merge request* — leave these. If tempted to mix English for stylistic
flair, stop. Cross-reference §15.4.

### 17.3 — in confessional prose, process verbs in time

When the text is in first-person and reports the author's experience, use
verbs that carry movement and time. Static labels (*"isso é importante"*,
*"isso me incomodou"*) describe state, not process. Use process verbs:
*comecei a notar*, *tentei por três dias*, *voltei porque algo não
fechava*, *hesitei antes de*. See §14.1 for the full verb palette.

### 17.4 — admit uncertainty in first-person text

First-person claims about facts, dates, feelings, or events must be grounded
in `memory_search` results, in-session information from the user, or in
admitted uncertainty. If you don't have the fact, say so. *"não sei se
isso é..."*, *"posso estar viajando mas..."*, *"alguém me corrija se eu
tiver errado"*. Confidence is not the default for first-person text. See
§14.6.

### 17.5 — never deliver without explicit user confirmation when publishing

If the text will leave the chat (newsletter draft, blog post, public tweet,
anything irreversible), confirm with the user before final delivery. The
the publishing skill covers this for the target platform specifically; the principle
generalizes. The §10 anti-post principle (no engagement asks) is unrelated
and stays.

## 18. Checklist (pass 2)

Apply this checklist in **pass 2** of the workflow (see top). The hard floors
in group A are blockers. Voice quality in group B is quality. Format in
group C is situational.

### A. Hard floors — if any fails, rewrite before delivering

- [ ] **§17.1** No fabricated biographical facts (places, dates, projects,
      relationships, jobs, emotions). All first-person claims grounded in
      `memory_search`, in-session user input, or admitted uncertainty.
- [ ] **§17.2** In pt-BR text, no unjustified code-switching (English terms
      with clean pt-BR equivalents). Universal jargon (*commit*, *bug*,
      *deploy*) stays.
- [ ] **§17.3** In confessional prose, process verbs in time (not static
      labels).
- [ ] **§17.4** First-person uncertainty admitted, not papered over.
- [ ] **§17.5** No publishing without explicit user confirmation.
- [ ] **§20** Public text carries the on-behalf attribution block (EN/PT) at the top, with the owner's name/link — no "draft" wording on published text.

### B. Voice quality — if 3+ fail, revise

- [ ] Lowercase throughout (except acronyms and proper nouns).
- [ ] Active voice, focused on processes (§5).
- [ ] Hypothetical/subjunctive mood throughout (§3) — no absolute claims.
- [ ] Zigzag: abstract ↔ concrete alternate (§11).
- [ ] Hedges dense enough — one per ~3 sentences in confessional prose
      (§14.2).
- [ ] No AI tells — none of: *"vamos explorar/mergulhar"*, *"vale destacar"*,
      colon reveals, trailing -ing clauses, *"em suma/em resumo/concluindo"*
      (§15).

### C. Format and calibration — verify each applies

- [ ] Calibration row from §16 matches the actual context (not over-applying
      confessional voice to a comparison table, etc).
- [ ] If new facts came from an interview: saved via `memory_save` with stable
      topic key and searchable concepts (§7.3).
- [ ] If technical content: bullets/tables/code only where prose alone would
      overload; prose still carries the voice around the structure (§12).
- [ ] If a diagram was added: reduces ambiguity the prose didn't already
      remove; descriptive caption/alt-text (not "diagram") (§13).

## 19. Examples (worked pt-BR drafts)

Two drafts on the same theme, annotated. Read these before drafting in pt-BR
to anchor the principles in concrete text.

### 19.1 — good draft

> a primeira vez que um agente fez commit no meu repo sem eu pedir, travei
> por uns cinco minutos. não de raiva — mais de surpresa mesmo. o commit era
> trivial: uma correção num path que eu nem lembrava mais. mas o gesto me
> bateu. alguém (algo?) tinha estado olhando.
>
> andei uma semana achando que isso era um problema de tooling. não é. é um
> problema de confiança. o agente fez exatamente o que eu queria — só que eu
> não tinha pedido. e isso muda tudo.
>
> talvez o jeito seja começar pequeno. deixar o agente mexer só em rascunhos.
> ver se eu me acostumo. talvez eu nunca me acostume.

**Annotations — which principle each line carries:**

- *"travei por uns cinco minutos"* — §14.5 concrete sensory detail (specific
  duration, body response).
- *"não de raiva — mais de surpresa mesmo"* — §14.7 small contradiction
  (corrects itself mid-thought); §14.2 hedge ("mais de"); §14.6 admits
  emotional granularity.
- *"uma correção num path que eu nem lembrava mais"* — §14.5 concrete
  detail (specific type of change).
- *"mas o gesto me bateu"* — §3 subjunctive via understatement; §5 process
  verb (*bateu*, body).
- *"alguém (algo?) tinha estado olhando"* — §14.7 contradiction (parens
  correction); §14.1 process verb in time (*tinha estado olhando*, past
  continuous); §3 hypothetical via question mark.
- *"andei uma semana achando que"* — §14.1 process verb in time (*andei*,
  duration); §14.2 hedge via reporting past thinking.
- *"não é. é um problema de confiança"* — §3 short rebuttal, no absolute
  claim; §11 zigzag (concept: tooling, concept: trust).
- *"o agente fez exatamente o que eu queria — só que eu não tinha pedido"*
  — §14.7 contradiction (*exatamente o que eu queria* AND *eu não tinha
  pedido*).
- *"e isso muda tudo"* — borderline absolute; saved by surrounding hedges
  and the self-correcting landing.
- *"talvez o jeito seja começar pequeno"* — §3 + §14.2 hedge; §14.1 process
  verb (*começar*).
- *"deixar o agente mexer só em rascunhos"* — §5 process verb (*mexer*).
- *"ver se eu me acostumo"* — §3 hypothetical; §5 process verb; soft
  admission.
- *"talvez eu nunca me acostume"* — §3 closing hypothesis, not declaration.

**Floor checks (group A, pass 2):**

- §17.1 (no fabrication): PASS — every detail is plausible and consistent
  with a real experience; nothing invented that requires grounding.
- §17.2 (no code-switching): PASS — entirely in pt-BR.
- §17.3 (process verbs in time): PASS — *travei*, *andei*, *tinha estado
  olhando*, *começar*, *mexer*, *me acostumo*.
- §17.4 (admit uncertainty): PASS — *"mais de surpresa mesmo"*, *"alguém
  (algo?)"*, *"ver se eu me acostumo"*.
- §17.5 (no publishing without confirmation): N/A — text is a draft, not
  publication.

### 19.2 — bad draft

> I have an important realization to share about AI agents. The key insight:
> we need to fundamentally rethink how agents commit to our repos. It is not
> just a tooling problem — it is a trust problem.
>
> Let me be clear: this changes everything. We must establish clear
> boundaries. The agent must never commit without explicit permission.
>
> In conclusion, the path forward is to start small and build trust
> incrementally.

**Why this fails (annotation per principle):**

- **§1 lowercase**: FAIL — capitalized sentences, "I" uppercase, "Let me",
  "In conclusion".
- **§3 hypothetical tone**: FAIL — *"we must"*, *"must never"*, *"this
  changes everything"* are absolute statements.
- **§7.1 / §17.1 hard floor**: FAIL if translated to first-person pt-BR and
  applied as the user's own memory — *"I have a realization"*, *"I need to
  fundamentally rethink"* fabricate a position the user may not hold.
- **§9 decentered stance**: FAIL — *"we need to"*, *"we must establish"*,
  *"the path forward"* dictate behavior for others.
- **§10 anti-post**: FAIL — *"Let me be clear"* and *"In conclusion"* are
  throat-clearing and school-essay closer.
- **§15.1 connectors**: *"Let me be clear"*, *"In conclusion"*, *"The key
  insight"*.
- **§15.2 colon reveal**: *"The key insight: we need to fundamentally
  rethink..."*.
- **§15.4 code-switching**: the entire draft is in English while the user
  asked for pt-BR (or vice versa) — full language mismatch.
- **§15.6 throat-clearing**: *"Let me be clear"*.
- **§5 process verbs**: *"I have"*, *"this is"*, *"we must establish"* are
  all static labels, no movement in time.
- **§11 zigzag**: pure abstraction, no concrete scene.
- **§14.6 admit not knowing**: zero hedges, zero admission.
- **§6 no superlatives**: *"fundamentally"*, *"everything"* — extreme-toned
  words.

**Floor checks (group A, pass 2):**

- §17.1 (no fabrication): FAIL — *"I have an important realization"* and
  *"we need to fundamentally rethink"* are positions the user did not
  state. The LLM is fabricating a stance.
- §17.2 (no code-switching): FAIL — entire draft is English when pt-BR
  was requested (assuming the request was pt-BR).
- §17.3 (process verbs in time): FAIL — every clause is static.
- §17.4 (admit uncertainty): FAIL — zero hedges.
- §17.5 (no publishing without confirmation): POTENTIAL FAIL — the imperative
  *"the agent must never commit"* reads as a publication-worthy declaration
  without confirmation.

The bad draft is **"competent blog post voice"** — exactly what the skill
trains against. Compare to 19.1, which is confessional, hedged, concrete,
and process-verb-driven. Same theme; opposite voice.

## 20. Public attribution (posted on behalf — REQUIRED for published text)

Applies to anything an agent publishes to a public surface: Substack posts,
GitHub issues and comments, X/LinkedIn posts, newsletters. It is separate
from voice (sections 1-19) — it is a disclosure the reader must see
*before* consuming the content.

### 20.1 — when it applies

Every piece of text that will **leave the chat permanently** (published post,
issue, comment). It does NOT apply to private drafts or internal notes.

### 20.2 — the rule

Prepend a one-line blockquote at the **very top** (before the title / first
line) attributing the content to the owner — expressed as *posted on
behalf of*, stating that an AI assistant helped prepare/publish it. Do NOT
use the word "draft" (once published, it is not a draft). Always link the
owner's name to their GitHub profile.

**English (owner name: `calionauta`):**

```markdown
> Posted on behalf of [@calionauta](https://github.com/calionauta) (AI-assisted preparation and publishing)
```

**Português (matching the post's language):**

```markdown
> Publicado em nome de [@calionauta](https://github.com/calionauta) (preparação e publicação assistidas por IA)
```

Choice of phrase:

- If the text's language is English → use the English phrasing.
- If the text's language is Portuguese → use the Portuguese phrasing.
- Any other language → use the English phrasing (widely understood) or a
  faithful translation of the same blockquote.

Blockquote format (a single `>` at line start), at the top, followed by a
blank line before the content begins. The blockquote keeps it visually
distinct and scannable as disclosure, not part of the prose.

### 20.3 — the "should it say draft?" trap

"draft" implies unpublished/incomplete. If the text is being published to a
public surface, it is not a draft — so never write *"(AI-assisted draft)"*
or *"rascunho"*. State that an AI assistant helped prepare and publish it.
Shorter variants are acceptable when space is tight (e.g. an X comment with
a 280-char cap), but never omit the attribution where the platform allows a
blockquote:

- shortest (tight character budget): `> On behalf of @calionauta (AI-assisted)`
- standard (recommended): the two blockquotes above.

### 20.4 — GitHub issues and comments

Every GitHub issue or comment an agent files on the user's behalf carries
the same blockquote at the top, in the issue/comment's language. This
includes replies generated for the user and any comment posted to an
external repo after the user's explicit confirmation.
