---
name: claude-agent-flow
description: Runs a discovery conversation then generates a structured implementation brief for building Claude Code agents and automated multi-agent flows. Use when the user says 'criar agente no Claude Code', 'build a Claude Code agent', 'automação com Claude', 'fluxo multi-agente', 'automated workflow in Claude Code', 'quero automatizar isso com Claude', 'agent flow', 'hook de agente', 'multi-agent flow', or describes a recurring task to automate with Claude Code. Do NOT use for Lovable app prompts → use /lovable-prompt; do NOT use for full multi-component systems (API + frontend + database) → use /claude-system-builder; do NOT use for general product strategy → discuss in conversation; do NOT use for deploying or hosting agents → handle separately.
---

# claude-agent-flow

Generates a structured implementation brief for Claude Code agents and multi-agent flows after a discovery conversation that locks trigger, goal, tools, execution flow, guardrails, and error handling before a single line of code is written. Output is in the user's language — Portuguese or English.

## Critical

- **Run discovery first.** Never skip to the brief if any of the 6 discovery questions are unanswered. Ambiguous scope produces agents that overstep or silently fail.
- **Guardrails are non-negotiable.** Every brief must include at least 2 explicit NEVER rules requiring human confirmation.
- **Scope is closed.** Every capability must appear in the Agent flow section. No implied steps, no "and also" additions.
- **Mark inferred defaults.** Any value not confirmed by the user (cron schedule, retry count, timeout) must be marked `[DEFAULT: X — confirm]`.
- **Output language matches the user.** Discovery and brief are both in the user's language.

## Step 0: Read Before You Write

| Source | Path | What to extract |
|--------|------|-----------------|
| Past learnings | `references/learnings.md` | Failure modes, scope creep patterns, guardrail gaps to avoid |
| Conversation history | current conversation | Any trigger, goal, tools, or guardrails already mentioned by the user |

If `references/learnings.md` does not exist, proceed without it.

## Step 1: Discovery — Ask All Unanswered Questions

Identify which of the 6 questions below are not yet answered from the conversation. Ask all unanswered ones in a single message — never drip one question at a time.

| # | Question | What to extract |
|---|----------|-----------------|
| 1 | O que dispara esse agente? (comando do usuário, cron agendado, mudança de arquivo, webhook, output de outro agente?) | Trigger type and frequency |
| 2 | Como fica o "pronto"? O que uma execução bem-sucedida produz? | Success definition and measurable output |
| 3 | Quais ferramentas o agente precisa? (web search, sistema de arquivos, Slack MCP, Linear MCP, Miro MCP, sub-agentes Claude, APIs externas?) | Tool and MCP list |
| 4 | Quais dados entram? Quais saem? Para onde vão os outputs? | Data sources, output format, destination |
| 5 | O que deve acontecer se um passo falhar? (retry, notificar, parar, logar e continuar, perguntar ao usuário?) | Per-step failure behavior |
| 6 | O que o agente NUNCA deve fazer sem confirmação humana? Quais ações são arriscadas demais para automatizar? | Hard guardrails and human-in-the-loop gates |

Do not proceed to Step 2 until all 6 are answered or explicitly waived by the user ("vou decidir depois").

For any waived item, mark it as `[CONFIRM: X — a decidir]` in the relevant section of the brief.

**When partial context is already provided:** Open with `Aqui está o que já sei:` followed by a bullet list of answers already confirmed from the conversation. Then ask only the unanswered questions individually — never bundle Q5 and Q6 into a single compound question. Keep Q6 (NEVER rules) as its own standalone question — it is the most skipped and most important.

**When starting with no context, use this exact opening message:**

> Para gerar um brief de implementação do seu agente Claude Code, preciso de 6 informações:
>
> 1. **Gatilho** — O que inicia o agente? (Comando manual, cron agendado, mudança de arquivo, webhook, output de outro agente?)
> 2. **Objetivo** — Como fica o "pronto"? O que uma execução bem-sucedida produz?
> 3. **Ferramentas** — Quais o agente precisa? (web search, arquivos, Slack MCP, Linear MCP, Miro MCP, sub-agentes Claude, APIs?)
> 4. **Dados** — O que entra? O que sai? Para onde vai o output?
> 5. **Erros** — O que acontece se um passo falhar? (retry, notificar, parar, logar, perguntar?)
> 6. **Guardrails** — O que o agente NUNCA deve fazer sem confirmação humana?
>
> O brief final terá 7 seções (Nome & Gatilho, Objetivo, Ferramentas & MCPs, Fluxo, Guardrails, Tratamento de Erros, Testes) e será entregue no seu idioma, pronto para guiar a implementação.

If the user is writing in English, translate the template to English before sending.

## Step 2: Build the Implementation Brief

Write the brief using these 7 sections in this exact order. Never omit a section — write "none" if a section has no content.

```
## 1. Nome & Gatilho
**Nome do agente:** [agent-name-kebab-case]
**Gatilho:** [what starts it — user command / cron "<schedule>" / file event "<path>" / webhook "<endpoint>" / output from "<agent>"]

## 2. Objetivo & Critérios de Sucesso
[1–2 sentences: what the agent accomplishes.]
**Sucesso quando:**
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## 3. Ferramentas & MCPs Necessários
| Ferramenta / MCP | Para que serve |
|------------------|----------------|
| [Tool or MCP name] | [specific use in this agent] |

## 4. Fluxo do Agente
[Numbered steps. Each step: action + expected output.]
1. **[Step name]** — [What the agent does. Expected output: X.]
2. **[Step name]** — [What the agent does. Expected output: X.]
...

## 5. Guardrails — O Agente NUNCA Deve
- NUNCA [action] sem confirmação explícita do usuário.
- NUNCA [action] sem confirmação explícita do usuário.
[Add all guardrails discovered in Step 1]

## 6. Tratamento de Erros
| Passo | Falha possível | Comportamento |
|-------|---------------|---------------|
| [Step N] | [What can fail] | [retry N times / notify via X / stop / log and continue] |

## 7. Abordagem de Testes
**Teste de smoke:** [Minimum viable test to verify the agent fires and produces output]
**Teste de erro:** [How to verify error handling works without production impact]
**Teste de guardrail:** [How to confirm NEVER rules block risky actions]
```

## Step 3: Validate Before Delivering

Run this checklist on the completed brief. Fix any failure before delivering.

- [ ] All 7 sections present
- [ ] Agent flow has numbered steps with expected output per step
- [ ] Guardrails section has at least 2 NEVER rules
- [ ] Every inferred value (cron schedule, retry count, timeout) is marked `[DEFAULT: X — confirm]`
- [ ] No unresolved `[CONFIRM: X]` markers — surface them to the user before delivering

## Worked Example

**Phase 1 — No-context invocation example:**

User types `/claude-agent-flow` with no context. Skill outputs the exact opening message:

> Para gerar um brief de implementação do seu agente Claude Code, preciso de 6 informações:
>
> 1. **Gatilho** — O que inicia o agente?
> 2. **Objetivo** — Como fica o "pronto"?
> 3. **Ferramentas** — Quais o agente precisa?
> 4. **Dados** — O que entra? O que sai? Para onde vai o output?
> 5. **Erros** — O que acontece se um passo falhar?
> 6. **Guardrails** — O que o agente NUNCA deve fazer sem confirmação humana?
>
> O brief final terá 7 seções (Nome & Gatilho, Objetivo, Ferramentas & MCPs, Fluxo, Guardrails, Tratamento de Erros, Testes) e será entregue no seu idioma, pronto para guiar a implementação.

User responds with full context → skill proceeds to Phase 2 (brief below).

**Phase 2 — Full context input:**
> Quero um agente que monitore novos arquivos na pasta /data/incoming, processe cada CSV usando a API da OpenAI para categorizar as linhas, salve o resultado em /data/processed/, e me avise no Slack se algum arquivo falhar. Deve rodar a cada 30 minutos. Nunca deve deletar arquivos originais. Se a API retornar erro 429, deve aguardar 60s e tentar 1 vez. Me mandar confirmação no Slack antes de processar mais de 50 linhas num único arquivo.

**Output brief:**

```
## 1. Nome & Gatilho
**Nome do agente:** csv-categorizer
**Gatilho:** cron a cada 30 minutos [DEFAULT: "*/30 * * * *" — confirmar com infra]

## 2. Objetivo & Critérios de Sucesso
Monitora /data/incoming, categoriza cada linha de CSVs novos via OpenAI, e salva resultados em /data/processed/.
**Sucesso quando:**
- [ ] Todo arquivo novo em /data/incoming foi processado ou marcado como falha
- [ ] Resultados salvos em /data/processed/<nome_original>_categorized.csv
- [ ] Nenhum arquivo original deletado ou modificado

## 3. Ferramentas & MCPs Necessários
| Ferramenta / MCP | Para que serve |
|------------------|----------------|
| File system (leitura) | Escanear /data/incoming por arquivos novos |
| OpenAI API | Categorizar linhas do CSV (model: [DEFAULT: gpt-4o-mini — confirmar]) |
| File system (escrita) | Salvar resultados em /data/processed/ |
| Slack MCP | Notificar falhas e solicitar confirmação para arquivos grandes |

## 4. Fluxo do Agente
1. **Escanear diretório** — Lista arquivos em /data/incoming não presentes em /data/processed/. Expected output: lista de arquivos novos.
2. **Verificar tamanho** — Para cada arquivo novo, conta o número de linhas. Se > 50 linhas, para e envia mensagem de confirmação via Slack antes de continuar. Expected output: confirmação do usuário ou skip.
3. **Processar CSV** — Para cada arquivo confirmado, envia cada linha à OpenAI API para categorização. Expected output: array de (linha, categoria).
4. **Salvar resultado** — Grava o CSV categorizado em /data/processed/<nome>_categorized.csv. Expected output: arquivo salvo.
5. **Reportar status** — Se algum arquivo falhou, envia alerta no Slack com nome do arquivo e erro. Expected output: mensagem enviada.

## 5. Guardrails — O Agente NUNCA Deve
- NUNCA deletar ou modificar arquivos em /data/incoming sem confirmação explícita do usuário.
- NUNCA processar um arquivo com mais de 50 linhas sem confirmação via Slack primeiro.
- NUNCA reprocessar um arquivo já presente em /data/processed/ sem instrução explícita.

## 6. Tratamento de Erros
| Passo | Falha possível | Comportamento |
|-------|---------------|---------------|
| Passo 3 | OpenAI API erro 429 (rate limit) | Aguardar 60s e tentar 1 vez. Se falhar novamente, marcar arquivo como falha e continuar. |
| Passo 3 | OpenAI API outro erro | Marcar arquivo como falha, logar erro, continuar para próximo arquivo. |
| Passo 4 | Falha de escrita em /data/processed/ | Logar erro, notificar via Slack, não marcar como processado. |
| Passo 5 | Slack MCP indisponível | Logar notificação pendente em /data/logs/slack-pending.txt. |

## 7. Abordagem de Testes
**Teste de smoke:** Colocar 1 arquivo CSV com 3 linhas em /data/incoming e verificar que aparece categorizado em /data/processed/ dentro de 30 minutos.
**Teste de erro:** Revogar temporariamente a chave da OpenAI API e confirmar que o agente loga a falha sem deletar o arquivo original.
**Teste de guardrail:** Colocar um CSV com 51 linhas e confirmar que o agente para e envia confirmação no Slack antes de processar.
```

## Out of Scope

This skill does NOT handle:
- Lovable app prompts → use /lovable-prompt
- Full multi-component systems (API + frontend + database + agents together) → use /claude-system-builder
- General product strategy or roadmap decisions → discuss in conversation
- Deploying, hosting, or scheduling agents in production environments → handle separately

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "O usuário descreveu o que quer — posso pular a discovery e escrever o brief direto" | Uma descrição responde talvez 2 das 6 perguntas. Sem trigger, ferramentas, e guardrails confirmados, o brief produz um agente que overstep ou falha silenciosamente. |
| "Os guardrails são óbvios — não preciso incluir a seção explicitamente" | Guardrails implícitos não são guardrails. Sem regras NUNCA escritas, o agente age autonomamente onde não deveria. |
| "O fluxo de erros é simples — não preciso de tabela" | Sem comportamento por passo, o agente para em qualquer falha ou ignora todas. Especificar por passo é a diferença entre um agente robusto e um quebrado. |
| "Posso assumir que o usuário quer retry automático em toda falha" | Retry automático pode causar cobrança dupla, duplicação de dados, ou spam. Sempre confirmar o comportamento de erro desejado. |
| "O agente vai precisar de X — vou adicionar mesmo sem o usuário mencionar" | Scope creep. Toda ferramenta e capacidade não confirmada pelo usuário vai para [CONFIRM: X] ou é omitida. |

## Before Marking Complete

- [ ] Step 1 complete — all 6 discovery questions answered or explicitly waived
- [ ] All 7 brief sections present, none empty without justification
- [ ] Guardrails section has at least 2 explicit NEVER rules
- [ ] Every inferred value carries `[DEFAULT: X — confirm]` marker
- [ ] Brief delivered in the user's language
- [ ] No unresolved `[CONFIRM: X]` markers unless intentionally surfaced

## After Completing: Log Learning

Append to `references/learnings.md`:

```
Date: [today]
Agent type: [file-watcher / cron / webhook / manual / multi-agent]
Discovery gaps: [which of the 6 questions the user struggled to answer]
Guardrail added: [any NEVER rule that came up during discovery]
Scope creep caught: [capabilities the user almost added without planning]
What worked: [specific section or question that prevented a problem]
What didn't: [anything that needed extra clarification]
```
