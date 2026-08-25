---
name: prd-router
description: Analisa um PRD e classifica se o produto deve ser construído no Lovable ou como software com Claude Code, propõe o destino com justificativa rastreável ao PRD, aguarda confirmação explícita, ativa /lovable-prompt ou /claude-system-builder, e ao final invoca /build-decisions para documentar as decisões. Use quando o usuário escrever "roteia esse PRD", "analisa esse PRD", "classifica esse PRD", "para onde vai esse PRD", "decide se uso Lovable ou Claude Code", "qual caminho esse PRD segue", "route this PRD", "analyze this PRD". Do NOT use para discovery de produto sem PRD → use /product-discovery. Do NOT use para criar prompt Lovable sem roteamento → use /lovable-prompt. Do NOT use para criar spec técnica sem roteamento → use /claude-system-builder. Do NOT use para documentar decisões de artefato já existente → use /build-decisions.
---

# prd-router

Recebe um PRD, classifica o destino (Lovable vs Software/Claude Code) com evidências rastreáveis ao texto, propõe ao usuário, aguarda confirmação explícita, ativa a skill correspondente, e encerra invocando /build-decisions. Nunca pula etapas. Nunca ativa skills sem confirmação.

## Critical

- **NUNCA ativar /lovable-prompt ou /claude-system-builder sem confirmação explícita do usuário no Step 3.** Confirmação implícita não conta.
- **NUNCA invocar /build-decisions sem o artefato da skill anterior estar completo e visível na conversa.**
- **Toda célula da tabela de classificação precisa citar evidência do PRD.** Célula com "não mencionado" é válida — célula com opinião sem rastreamento não é.
- **Se o PRD for ambíguo, fazer as 3 perguntas do Step 2B antes de propor.** Nunca propor destino com evidências insuficientes.
- **Aceitar a escolha do usuário se divergir da proposta.** A proposta é uma recomendação, não uma imposição.

## Step 0: Localizar o PRD

| Source | Path/Location | What to extract |
|--------|--------------|-----------------|
| PRD | Conversa atual (texto colado) ou arquivo referenciado | Texto completo do PRD |
| Learnings | `references/learnings.md` | Padrões de classificação anteriores, critérios que induziram erro |

Se nenhum PRD for encontrado na conversa: **parar imediatamente** e exibir:

> Não encontrei um PRD na conversa. Cole o PRD ou informe o caminho do arquivo.
>
> Após receber o PRD, farei:
> 1. **Classificação** — tabela de 5 critérios com evidências rastreáveis ao texto
> 2. **Proposta** — destino recomendado + argumento contrário + kill criteria
> 3. **Confirmação** — "A construção será para Lovable ou software normal?"
> 4. **Ativação** — `/lovable-prompt` ou `/claude-system-builder` com o PRD como contexto
> 5. **Documentação** — `/build-decisions` ao final para registrar regras e decisões
>
> Se ainda não tiver um PRD, use `/product-discovery` para estruturar o problema primeiro.

Se o PRD tiver menos de 200 palavras: continuar, mas sinalizar no Step 2 que o PRD é curto e considerar ambíguo por padrão.

## Step 1: Extrair contexto do PRD

Ler o PRD completo. Identificar internamente:
- Nome/descrição do produto
- Usuários-alvo
- Funcionalidades do MVP
- Menções a backend, integrações, infraestrutura, workers, filas
- Stack tecnológica (se mencionada)

## Step 2: Classificar destino

Preencher a tabela com evidências diretas do PRD. Citar trecho ou seção — nunca parafrasear sem rastreamento.

| Critério | Evidência no PRD | Aponta para |
|----------|-----------------|-------------|
| Complexidade de backend | [trecho do PRD ou "não mencionado"] | Lovable / Software |
| Número de serviços | [trecho do PRD ou "não mencionado"] | Lovable / Software |
| Integrações externas | [trecho do PRD ou "não mencionado"] | Lovable / Software |
| Infraestrutura | [trecho do PRD ou "não mencionado"] | Lovable / Software |
| Escopo do MVP | [trecho do PRD ou "não mencionado"] | Lovable / Software |

Referência de decisão por critério:

| Critério | Indica Lovable | Indica Software (Claude Code) |
|----------|---------------|-------------------------------|
| Backend | Supabase suficiente (auth, CRUD, RLS) | Lógica customizada, workers, jobs agendados |
| Serviços | 1 app web | 2+ serviços, microserviços, APIs customizadas |
| Integrações | Nenhuma ou 1 simples | 2+, OAuth complexo, webhooks, streams |
| Infraestrutura | Zero config / Supabase gerenciado | CI/CD, Docker, Cloudflare, GitHub Actions |
| Escopo do MVP | Interface funcional em ~1 sessão Lovable | Arquitetura com 2+ dias de Claude Code |

Contar maioria → destino candidato. Se empate ou ambiguidade: ir para Step 2B.

**Step 2B — Contexto adicional (PRD ambíguo):**

Fazer estas 3 perguntas antes de propor:
1. "Esse produto precisa de lógica de backend além de CRUD e autenticação?"
2. "Tem alguma integração que precisa de webhook, fila ou processamento assíncrono?"
3. "O MVP precisa estar em produção com URL pública e domínio customizado, ou é um protótipo funcional?"

Aguardar resposta antes de continuar para Step 3.

## Step 3: Propor destino e aguardar confirmação

Apresentar a proposta neste formato exato:

---

**Classificação do PRD — [nome do produto]**

| Critério | Evidência no PRD | Aponta para |
|----------|-----------------|-------------|
| Complexidade de backend | [evidência] | [Lovable / Software] |
| Número de serviços | [evidência] | [Lovable / Software] |
| Integrações externas | [evidência] | [Lovable / Software] |
| Infraestrutura | [evidência] | [Lovable / Software] |
| Escopo do MVP | [evidência] | [Lovable / Software] |

**Destino proposto: [Lovable / Software — Claude Code]**

**Porquê:** [2–3 frases citando evidências específicas do PRD. Sem generalizações.]

**Argumento mais forte para o outro caminho:** [Nomear o argumento mais sólido para a alternativa — citar a evidência mais relevante do PRD que aponta para o outro lado. Nunca inventar um argumento fraco.]

**O que mudaria essa decisão:**
- [Condição 1 que inverteria o destino]
- [Condição 2 que inverteria o destino]
- [Condição 3 que inverteria o destino]

**A construção será para Lovable ou software normal?**

---

Aguardar confirmação explícita. Confirmação válida = usuário nomeia o destino ("Lovable" ou "software") ou escreve que concorda. Se ambíguo, perguntar de novo antes de prosseguir.

Se o usuário escolher diferente da proposta: aceitar, registrar a escolha, prosseguir com o destino escolhido.

## Step 4: Ativar skill alvo

**Somente após confirmação explícita no Step 3.**

- Destino = Lovable → invocar `/lovable-prompt` com o PRD como contexto
- Destino = Software → invocar `/claude-system-builder` com o PRD como contexto

Aguardar a skill gerar o artefato completo antes de continuar.

## Step 5: Invocar /build-decisions

**Somente após o artefato do Step 4 estar completo e visível na conversa.**

Invocar `/build-decisions` com o artefato gerado. Resultado esperado: 3 tabelas no Miro + doc sumário.

## Worked Example

**Phase 1 — Sem PRD (invocação direta sem contexto):**

Usuário: `/prd-router`

Output:
> Não encontrei um PRD na conversa. Cole o PRD ou informe o caminho do arquivo.
>
> Após receber o PRD, farei:
> 1. **Classificação** — tabela de 5 critérios com evidências rastreáveis ao texto
> 2. **Proposta** — destino recomendado + argumento contrário + kill criteria
> 3. **Confirmação** — "A construção será para Lovable ou software normal?"
> 4. **Ativação** — `/lovable-prompt` ou `/claude-system-builder` com o PRD como contexto
> 5. **Documentação** — `/build-decisions` ao final para registrar regras e decisões
>
> Se ainda não tiver um PRD, use `/product-discovery` para estruturar o problema primeiro.

---

**Phase 2 — PRD de app de gestão de tarefas:**

Usuário: [cola PRD de ~400 palavras: app web TaskFlow, auth por e-mail, CRUD de tarefas com labels e filtros, persistência no Supabase, sem integrações externas]

Output:

**Classificação do PRD — TaskFlow**

| Critério | Evidência no PRD | Aponta para |
|----------|-----------------|-------------|
| Complexidade de backend | "Persistência no Supabase com autenticação por e-mail e RLS por usuário" | Lovable |
| Número de serviços | "Um único app web" | Lovable |
| Integrações externas | "Nenhuma integração mencionada no MVP" | Lovable |
| Infraestrutura | "Sem menção a deploy, CI/CD ou infraestrutura customizada" | Lovable |
| Escopo do MVP | "CRUD de tarefas com labels e filtros — interface funcional" | Lovable |

**Destino proposto: Lovable**

**Porquê:** O PRD descreve um app web com Supabase para auth e persistência, sem lógica de backend customizada, workers ou integrações externas. O MVP é uma interface funcional que Lovable entrega em 1 sessão com a stack React + TypeScript + Supabase.

**Argumento mais forte para Software (Claude Code):** Se o sistema de labels evoluir para tags compartilhadas entre times com permissões granulares, o RLS do Supabase pode não ser suficiente. O PRD não menciona esse cenário, mas seria o próximo passo mais provável de escala.

**O que mudaria essa decisão:**
- Necessidade de processamento assíncrono (ex: notificações por e-mail agendadas)
- Integração externa com OAuth ou webhook
- Requisito de domínio customizado com CI/CD em produção

**A construção será para Lovable ou software normal?**

## Out of Scope

This skill does NOT handle:
- Discovery de produto sem PRD → use /product-discovery
- Geração de prompt Lovable sem roteamento → use /lovable-prompt diretamente
- Geração de spec técnica sem roteamento → use /claude-system-builder diretamente
- Documentação de artefato já existente → use /build-decisions diretamente
- Deploy, configuração de infraestrutura ou CI/CD → tratar separadamente

## Cross-Skill Routing

- PRD classificado como Lovable + confirmado → ativar `/lovable-prompt`
- PRD classificado como Software + confirmado → ativar `/claude-system-builder`
- Artefato gerado e completo → ativar `/build-decisions`
- Sem PRD + usuário quer estruturar o problema → recomendar `/product-discovery`

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "O PRD é claramente para Lovable — não preciso preencher a tabela" | A tabela é o artefato da classificação. Sem ela o usuário não pode avaliar nem contestar a proposta. Sempre preencher todos os 5 critérios com evidências. |
| "O usuário disse 'pode ir' — vou ativar a skill" | Confirmação válida = usuário nomeia o destino ou escreve que concorda explicitamente. "Pode ir" ambíguo exige reconfirmação. |
| "O PRD é ambíguo mas tenho intuição — vou propor assim mesmo" | Intuição sem evidência produz argumentos que o usuário não consegue contestar. Se ambíguo, fazer as 3 perguntas do Step 2B primeiro. |
| "O artefato foi gerado — posso invocar /build-decisions" | Verificar que o artefato está completo e visível na conversa. Se a skill ainda está em execução ou produziu saída parcial, aguardar. |
| "O 'argumento mais forte para o outro caminho' é redundante" | Omiti-lo força o usuário a imaginar os riscos. Nomear o argumento mais forte é o que diferencia uma proposta honesta de uma venda. |

## Before Marking Complete

- [ ] Step 0: PRD localizado — ou decline determinístico exibido se ausente
- [ ] Step 2: Tabela preenchida com evidências rastreáveis ao PRD para todos os 5 critérios
- [ ] Step 3: Proposta apresentada com justificativa + argumento contrário + kill criteria + pergunta de confirmação
- [ ] Step 3: Confirmação explícita do usuário recebida antes de prosseguir
- [ ] Step 4: Skill ativada somente após confirmação
- [ ] Step 5: /build-decisions invocada somente após artefato completo na conversa

## After Completing: Log Learning

Append to `references/learnings.md`:
```
Date: [YYYY-MM-DD]
PRD type: [app web / sistema multi-serviço / ambíguo]
Destino classificado: [Lovable / Software / Ambíguo → Step 2B]
Usuário concordou com proposta: [sim / não — o que escolheu]
Critério mais decisivo: [qual dos 5 foi determinante]
Step 2B ativado: [sim / não]
O que funcionou: [parte do fluxo que ficou clara]
O que não funcionou: [onde houve hesitação ou dúvida]
```
