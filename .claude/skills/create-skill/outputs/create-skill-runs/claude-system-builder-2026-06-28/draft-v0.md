---
name: claude-system-builder
description: Runs a structured discovery conversation then generates a technical spec and phased implementation plan for building a software system through Claude Code — covering stack, components, data models, integrations, security constraints, and DO NOT rules. Use when the user says 'criar sistema pelo Claude Code', 'build a system with Claude Code', 'quero implementar um sistema', 'spec técnica para o Claude', 'architecture plan for Claude Code', 'plano de implementação', 'implementar um backend', 'system spec for Claude Code', 'quero construir uma API', or 'full stack com Claude Code'. Do NOT use for Lovable web apps (React + Supabase) → use /lovable-prompt; do NOT use for automated agent/flow workflows → use /claude-agent-flow; do NOT use for general product strategy → discuss in conversation; do NOT use for single scripts or one-off one-file tasks → write the prompt directly.
---

# claude-system-builder

Generates a structured technical spec and phased implementation plan for building a software system through Claude Code. Runs a 7-question discovery first, then produces a self-contained document Claude Code can execute without follow-up questions. Output is in the user's language.

## Critical

- **Run discovery first.** Never skip to the spec if any of the 7 discovery questions are unanswered. Ambiguous scope causes Claude Code to build the wrong thing or over-engineer in the wrong direction.
- **Output is in the user's language.** Discovery and spec are both delivered in whatever language the user is using.
- **All inferred values carry a [DEFAULT] marker.** Any tech stack version, configuration value, timeout, or infrastructure parameter not supplied by the user must appear as `[DEFAULT: X — confirm]`. Never let training-data guesses pass as user-confirmed facts.
- **Scope is closed.** Every component, endpoint, and integration must be explicitly listed. "And also" additions during implementation cause scope creep — prevent it here.
- **DO NOT rules are non-negotiable.** Include at least 5 universal DO NOT rules in every spec plus any discovered during the conversation.
- **Implementation phases are sequential.** Each phase must list what Claude Code builds AND what is explicitly out of that phase. Unbounded phases produce scope creep.

## Step 0: Read Before You Write

| Source | Path | What to extract |
|--------|------|-----------------|
| Past learnings | `references/learnings.md` | Failure patterns and scope creep signals to watch for |
| User conversation | conversation context | Answers to the 7 discovery questions (partial or full) |

If `references/learnings.md` does not exist, proceed without it.

**[DEFAULT] rule:** Any value not supplied by the user and not found in the read-first files (versions, port numbers, timeout values, replica counts, SLO targets, config params) must be marked `[DEFAULT: X — confirm]` in the output spec. Never silently fill in training-data defaults.

## Step 1: Discovery — Ask All Unanswered Questions

Identify which of the 7 questions below are not yet answered from the conversation. Ask all unanswered ones in a single message — never drip one question at a time.

| # | Question | What to extract |
|---|----------|-----------------|
| 1 | What is this system? What problem does it solve and for whom? | System purpose + user persona |
| 2 | Who uses it? Internal team, API consumers, end users, admin only? | User types + access model |
| 3 | What are the main components? (REST API, frontend, database, message queue, cron worker, CLI, admin panel?) | Component list |
| 4 | Language and framework? Database? Hosting/infra? CI/CD? | Full tech stack |
| 5 | External APIs, auth provider, payments, storage, email, observability? | Integration list |
| 6 | Auth required? Data sensitivity (PII, financial, health)? Compliance requirements? | Security constraints |
| 7 | What exactly should Claude Code implement? What's already built or out of scope? | Implementation boundary |

Do not proceed to Step 2 until all 7 are answered or explicitly waived by the user ("I'll decide later on X").

For any waived item, mark it as `[CONFIRM: X — to be decided]` in the relevant spec section.

**When starting with no context, use this exact opening message:**

> Para criar uma spec técnica e plano de implementação para o Claude Code, preciso de 7 informações:
>
> 1. **Sistema** — O que é esse sistema? Que problema resolve e para quem?
> 2. **Usuários** — Quem usa? Time interno, consumidores de API, usuários finais, admin?
> 3. **Componentes** — Quais são as partes principais? (API REST, frontend, banco de dados, fila, worker, CLI, painel admin?)
> 4. **Stack** — Linguagem e framework? Banco de dados? Hosting/infra? CI/CD?
> 5. **Integrações** — APIs externas, auth provider, pagamentos, storage, email, observabilidade?
> 6. **Segurança** — Auth obrigatório? Dados sensíveis (PII, financeiro, saúde)? Requisitos de compliance?
> 7. **Escopo para o Claude Code** — O que exatamente o Claude Code deve implementar? O que já existe ou está fora do escopo?
>
> A spec final terá 8 seções (Visão geral, Stack, Componentes, Modelos de dados, Contratos de integração, Segurança, Fases de implementação, Regras DO NOT) e será entregue no seu idioma.

If the user is writing in English, translate the template to English before sending.

## Step 2: Generate the Technical Spec

Write the spec in the user's language using these 8 sections in this exact order. Never omit a section — write "none" if a section has no content.

For any section where the user waived or didn't specify a value, still write the complete section using `[DEFAULT: X — confirm]` for specific values and `[CONFIRM: X — to be decided]` for structural decisions. Never leave a section thin or empty.

```
## 1. Visão Geral do Sistema  [or "System Overview" in English]
[2–3 sentences: what the system does, what problem it solves, who uses it.]

## 2. Stack Técnica  [or "Tech Stack"]
- Linguagem: [language + version or DEFAULT]
- Framework: [framework + version or DEFAULT]
- Banco de dados: [database + version or DEFAULT]
- Hosting: [platform or DEFAULT]
- CI/CD: [tool or DEFAULT / none]
- Pacotes adicionais: [list or none]

## 3. Componentes e Responsabilidades  [or "Components & Responsibilities"]
- [Nome do componente]: [one-sentence job description]
- [Nome do componente]: [one-sentence job description]

## 4. Modelos de Dados  [or "Data Models"]
### [Entidade / Entity]
| Campo / Field | Tipo / Type | Notas / Notes |
|-------|------|-------|
| id | uuid / int | PK |
| [field] | [type] | [constraint or relationship] |

## 5. Contratos de Integração  [or "Integration Contracts"]
| Integração | Auth | Operação | Notas |
|------------|------|----------|-------|
| [name] | [API key / OAuth / JWT] | [what it does] | [limits or error handling] |

## 6. Restrições de Segurança  [or "Security Constraints"]
- Modelo de auth: [JWT / session / API key / none]
- Permissões: [RLS rules / role-based access / public]
- Validação de entrada: [required fields, sanitization rules]
- Segredos: [env vars / vault / none — where secrets live]

## 7. Fases de Implementação  [or "Implementation Phases"]

### Fase 1 — [Nome]  [or "Phase 1 — [Name]"]
**O Claude Code constrói:**
- [item específico]
- [item específico]

**Fora desta fase:**
- [what is NOT built yet]

**Critérios de aceite:**
- [ ] [concrete, verifiable check]
- [ ] [concrete, verifiable check]

[Repeat for each phase]

## 8. Regras DO NOT  [or "DO NOT Rules"]
- Nunca [rule 1]  [or "Never [rule 1]"]
- Nunca [rule 2]
- Nunca [rule 3]
- Nunca [rule 4]
- Nunca [rule 5]
```

## Worked Example

**Input (discovery answers):**
- System: Task management API for a B2B SaaS. Teams create workspaces, projects, and tasks with deadline tracking.
- Users: Team members (standard) and workspace admins. ~50 workspaces at launch.
- Components: REST API, PostgreSQL database, cron worker for deadline reminders.
- Stack: Node.js + TypeScript, Express 4, PostgreSQL 15, Docker, Railway.
- Integrations: SendGrid for email deadline reminders.
- Security: JWT auth required on all routes; data scoped by workspace_id.
- Claude Code scope: Build REST API + DB schema + migrations + cron worker. Frontend is separate.

**Output:**

---

## 1. Visão Geral do Sistema
API REST para gestão de tarefas em equipes B2B. Permite que times organizem trabalho em workspaces, projetos e tarefas com prazos e atribuições. Usada por membros de equipe e admins de workspace via qualquer frontend ou cliente HTTP.

## 2. Stack Técnica
- Linguagem: Node.js + TypeScript [DEFAULT: TypeScript 5.x — confirm]
- Framework: Express 4
- Banco de dados: PostgreSQL 15
- Hosting: Railway [DEFAULT: single-region — confirm]
- CI/CD: none (fora do escopo)
- Pacotes adicionais: `pg`, `jsonwebtoken`, `node-cron`, `@sendgrid/mail`, `zod`

## 3. Componentes e Responsabilidades
- **API server** (Express): trata auth, todos os endpoints REST, validação via Zod, aplica escopo por workspace.
- **PostgreSQL**: armazena todo o estado persistente — usuários, workspaces, projetos, tarefas.
- **Cron worker** (node-cron, mesmo processo): roda diariamente, consulta tarefas com prazo em 24h, dispara email via SendGrid por assignee.

## 4. Modelos de Dados

### users
| Campo | Tipo | Notas |
|-------|------|-------|
| id | uuid | PK |
| email | text | único, not null |
| password_hash | text | bcrypt |
| created_at | timestamptz | default now() |

### workspaces
| Campo | Tipo | Notas |
|-------|------|-------|
| id | uuid | PK |
| name | text | not null |
| owner_id | uuid | FK users.id |

### workspace_members
| Campo | Tipo | Notas |
|-------|------|-------|
| workspace_id | uuid | FK workspaces.id |
| user_id | uuid | FK users.id |
| role | text | 'admin' ou 'member' |

### projects
| Campo | Tipo | Notas |
|-------|------|-------|
| id | uuid | PK |
| workspace_id | uuid | FK workspaces.id |
| name | text | not null |

### tasks
| Campo | Tipo | Notas |
|-------|------|-------|
| id | uuid | PK |
| project_id | uuid | FK projects.id |
| title | text | not null |
| status | text | 'todo', 'in_progress', 'done' |
| assignee_id | uuid | FK users.id, nullable |
| due_date | date | nullable |

## 5. Contratos de Integração
| Integração | Auth | Operação | Notas |
|------------|------|----------|-------|
| SendGrid | API key (env: SENDGRID_API_KEY) | POST /v3/mail/send — email de aviso de prazo | [DEFAULT: plano gratuito 100 emails/dia — confirmar plano] |

## 6. Restrições de Segurança
- Modelo de auth: JWT [DEFAULT: HS256 — confirmar algoritmo de assinatura], header `Authorization: Bearer <token>` em todas as rotas protegidas.
- Permissões: toda query filtra por `workspace_id` — aplicar em middleware, não por endpoint. Role 'admin' obrigatório para deleção de workspace e gestão de membros.
- Validação de entrada: todos os bodies validados com Zod antes de tocar na lógica de negócio. Rejeitar campos desconhecidos.
- Segredos: `SENDGRID_API_KEY`, `JWT_SECRET`, `DATABASE_URL` em variáveis de ambiente. Nunca hardcoded.

## 7. Fases de Implementação

### Fase 1 — Fundação
**O Claude Code constrói:**
- Schema do banco + migrations (5 tabelas acima)
- Boilerplate Express + handler de erros
- Auth: `POST /auth/register`, `POST /auth/login` (retorna JWT)
- Middleware de auth (verifica JWT + anexa usuário ao request)
- Workspace CRUD: `POST /workspaces`, `GET /workspaces/:id`, `DELETE /workspaces/:id`
- Membros: `POST /workspaces/:id/members`, `DELETE /workspaces/:id/members/:userId`

**Fora desta fase:**
- Endpoints de projects e tasks
- Cron worker e integração com SendGrid

**Critérios de aceite:**
- [ ] `POST /auth/login` retorna JWT válido para usuário seedado
- [ ] `GET /workspaces/:id` retorna 401 sem token, 403 para workspace errado
- [ ] `npm run migrate` aplica todas as migrations em instância PostgreSQL limpa

### Fase 2 — Domínio Principal
**O Claude Code constrói:**
- Project CRUD: `POST /workspaces/:id/projects`, `GET /workspaces/:id/projects`, `DELETE /projects/:id`
- Task CRUD: `POST /projects/:id/tasks`, `GET /projects/:id/tasks`, `PATCH /tasks/:id`, `DELETE /tasks/:id`
- Filtro de tasks por `status` e `assignee_id` via query params

**Fora desta fase:**
- Cron worker e envio de email
- Anexos de arquivo ou comentários

**Critérios de aceite:**
- [ ] `POST /projects/:id/tasks` cria task escopada ao workspace do projeto
- [ ] `GET /projects/:id/tasks?status=todo` retorna apenas tasks correspondentes
- [ ] Usuário do workspace A não consegue ler tasks do workspace B

### Fase 3 — Worker e Notificações
**O Claude Code constrói:**
- Worker `cron.js` com `node-cron` [DEFAULT: roda às 08:00 diariamente — confirmar horário]
- Query SQL: tasks com `due_date = CURRENT_DATE + 1`, `status != 'done'`, `assignee_id NOT NULL`
- Chamada SendGrid: um email por assignee com lista de tasks com prazo amanhã
- Inicialização do worker em `app.ts`

**Fora desta fase:**
- Templates HTML para email (usar texto plano)
- Preferências de notificação ou opt-out do usuário
- Digest agrupado vs. email por task

**Critérios de aceite:**
- [ ] Worker loga "Nenhuma task com prazo amanhã" quando não há nenhuma
- [ ] Worker envia um email por assignee único (não um por task)
- [ ] `SENDGRID_API_KEY` ausente gera warning no startup, não crash

## 8. Regras DO NOT
- Nunca hardcode segredos, API keys ou connection strings — usar variáveis de ambiente.
- Nunca usar `any` em TypeScript — todos os tipos devem ser explícitos.
- Nunca bypassar o middleware de auth em rotas protegidas.
- Nunca interpolar strings em SQL — usar queries parametrizadas via `pg`.
- Nunca acessar dados de outro workspace — aplicar filtro de `workspace_id` na query, não no caller.
- Nunca implementar funcionalidades fora do escopo acima sem confirmação explícita do usuário.

---

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "The user gave me enough context — I can skip discovery and go straight to the spec." | The 7 questions exist because what users describe and what they mean often diverge. A missing question produces a spec Claude Code implements incorrectly. Always surface all unanswered questions first. |
| "This stack is standard enough — I don't need to mark defaults." | Defaults that look confirmed get hardcoded into migrations, Docker configs, and CI pipelines. `[DEFAULT]` markers force a confirm step that prevents silent mismatches later. |
| "I'll write implementation phases as a short list — scope is obvious." | Unbounded phases are the #1 source of scope creep. Each phase must list explicit "out of this phase" items. Obvious scope is only obvious to the person who wrote the spec. |
| "The user just wants a quick plan — I'll skip the data models." | Claude Code infers schema from whatever the spec implies. Unspecified fields get invented. Specify the data models so Claude Code builds what the user actually needs. |
| "I'll add DO NOT rules at the end if there's time." | DO NOT rules prevent the most expensive mistakes (hardcoded secrets, auth bypasses, SQL injection). They are non-negotiable and never optional. |

## Exit Checklist

Do not consider this task finished until all of the following are true:

- [ ] All 7 discovery questions answered or explicitly waived with `[CONFIRM]` markers
- [ ] Spec contains all 8 sections — none omitted
- [ ] Every inferred stack version, config value, or infrastructure parameter carries `[DEFAULT: X — confirm]`
- [ ] Each implementation phase has: what Claude Code builds, what is out of that phase, and acceptance criteria
- [ ] DO NOT rules include at least 5 items
- [ ] Any out-of-scope request detected (Lovable app, agent workflow) was surfaced before generating the spec
- [ ] Output is in the user's language

## Out of Scope

This skill does NOT handle:

- Lovable web apps (React + Supabase, AI-generated UI) → use /lovable-prompt
- Automated agent/flow workflows → use /claude-agent-flow
- General product strategy or roadmap → discuss directly in conversation
- Single-file scripts or one-off tasks → write the prompt directly without a skill
- Implementing the system (this skill produces a spec, not code) → hand the spec to Claude Code

## Cross-Skill Routing

After discovery, route before generating the spec if:
- User describes a web app to be built via Lovable → stop and recommend /lovable-prompt
- User describes an automated multi-agent or flow workflow → stop and recommend /claude-agent-flow

## After Completing: Log Learning

Append one entry to `references/learnings.md`:

```
Date: [today's date]
Input type: [no-context / partial / full]
What worked: [specific pattern that produced good output]
What didn't: [what failed or needed correction]
Edge case: [anything unexpected about this run]
```
