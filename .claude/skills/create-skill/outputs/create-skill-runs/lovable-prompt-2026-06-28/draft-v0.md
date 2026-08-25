---
name: lovable-prompt
description: Generates a structured, ready-to-paste English prompt for Lovable (AI web app builder) after a discovery conversation that locks scope, stack, design system, security constraints, and DO NOT guardrails. Use when the user says 'write a Lovable prompt', 'help me prompt Lovable', 'quero criar no Lovable', 'novo projeto no Lovable', 'build an app with Lovable', 'prompt para o Lovable', 'criar app no Lovable', 'prototipar com Lovable', or 'start a Lovable build'. Do NOT use for general product strategy → discuss in conversation; do NOT use for Lovable bug fixing or feature iterations after initial build → continue in Lovable chat directly; do NOT use for non-Lovable projects (Cursor, Bolt, raw Vite) → write the prompt manually.
---

# lovable-prompt

Generates a production-ready English prompt for Lovable after a structured discovery that locks scope, stack, design system, security constraints, and guardrails before Lovable writes a single line of code. The prompt is always in English — Lovable produces more robust React/TypeScript code, follows conventions better, and makes fewer interpretation errors from English inputs.

## Critical

- **Run discovery first.** Never skip to the prompt if any of the 6 discovery questions are unanswered. Ambiguous scope causes Lovable to hallucinate features.
- **Output prompt is always in English.** Discovery can happen in any language. Inform the user, then write the prompt in English regardless.
- **Scope is closed.** Every feature must appear in the Scope section. No implied features, no "and also" additions.
- **DO NOT rules are non-negotiable.** Include the 5 universal DO NOT rules in Step 2 plus any discovered in Step 1.
- **Design system is always declared.** Even when the user says "default is fine" — write it out explicitly. Omitting it lets Lovable choose arbitrarily.
- **Security section is always present.** Every app with a database needs it, even when the data is not sensitive.

## Step 0: Read Before You Write

| Source | Path | What to extract |
|--------|------|-----------------|
| Discovery answers | conversation | Problem, users, MVP features, stack, design prefs, integrations |
| Past learnings | references/learnings.md | Failure modes and scope creep patterns to avoid |

If `references/learnings.md` does not exist, proceed without it.

## Step 1: Discovery — Ask All Unanswered Questions

Identify which of the 6 questions below are not yet answered from the conversation. Ask all unanswered ones in a single message — never drip one question at a time.

| # | Question | What to extract |
|---|----------|-----------------|
| 1 | What pain point does this solve? Who feels it? | Problem statement + user persona |
| 2 | Who logs in? Internal team, B2B customers, B2C users? | Auth model, user volume expectation |
| 3 | What must work in v1? What is explicitly out of v1? | Feature list (in) + exclusion list (out) |
| 4 | Backend: Supabase? Auth provider? Payments? External APIs? | Stack decisions |
| 5 | Brand colors, fonts, tone? Or shadcn/ui defaults? | Design system spec |
| 6 | External integrations: webhooks, APIs, third-party services? | Integration list and auth method |

Do not proceed to Step 2 until all 6 are answered or explicitly waived by the user ("I'll decide later on X").

For any waived item, mark it as `[CONFIRM: X — to be decided]` in the relevant section of the prompt.

## Step 2: Build the English Prompt

Write the prompt in English using these 7 sections in this exact order. Never omit a section — write "none" if a section has no content.

```
## Context
[1–2 sentences: what the app does, who uses it, what problem it solves.]

## Stack
- Framework: React + TypeScript + Vite
- Styling: Tailwind CSS + shadcn/ui (components only — no other component library)
- Backend: [Supabase / none / specify]
  - Auth: [Supabase Auth / Clerk / none]
  - Database: [PostgreSQL via Supabase / none]
  - Storage: [Supabase Storage / none]
  - Edge Functions: [yes / no]
- Additional packages: [react-hook-form, zod, stripe-js, etc. / none]

## Design System
- Component library: shadcn/ui
- Color palette: [hex values / "shadcn/ui default"]
- Typography: [font name / "shadcn/ui default (Inter)"]
- Tone: [professional / startup / casual / specify]
- Dark mode: [yes / no / system]

## Scope — Build exactly these features
[Numbered list. Each item = one user story or screen. Cap at 10 items for v1.]
1. ...
2. ...

## Out of v1 — Do not build
[Items explicitly excluded. At least 1 entry required to prevent Lovable from guessing what comes next.]
- ...

## Security Constraints
- Authentication: [required — specify provider / not required]
- Row-level security: [table-name — policy intent / none]
- Input validation: [zod on all forms / specify / none]
- Sensitive data: [describe PII or sensitive fields / none]

## DO NOT
- DO NOT add any feature not listed in Scope.
- DO NOT use any component library other than shadcn/ui.
- DO NOT generate placeholder content, lorem ipsum, or stub data.
- DO NOT add analytics, telemetry, or tracking scripts.
- DO NOT install packages not listed in the Stack section.
[Add discovery-specific constraints here]
```

## Step 3: Validate Before Delivering

Run this checklist on the completed prompt. Fix any failure before delivering.

- [ ] All 7 sections present (Context, Stack, Design System, Scope, Out of v1, Security, DO NOT)
- [ ] Prompt is written entirely in English
- [ ] Scope is a numbered list — no vague items (e.g., "user settings" must specify which settings)
- [ ] "Out of v1" has at least 1 exclusion
- [ ] DO NOT has at least 5 rules (the 5 universal ones are mandatory)
- [ ] No unresolved `[CONFIRM: X]` markers — surface them to the user before delivering

## Worked Example

**Discovery input (in Portuguese):**
> Quero uma ferramenta interna para o time de CS rastrear chamadas de suporte. Login com email. Dashboard com tickets abertos. Supabase pro backend. Design padrão. Sem integrações externas por agora.

**Output prompt (English, ready-to-paste in Lovable):**

```
## Context
An internal customer support tracking tool for CS agents. Agents log in with email, view a dashboard of open support tickets, and manage ticket status. Replaces spreadsheets with a focused, minimal web app.

## Stack
- Framework: React + TypeScript + Vite
- Styling: Tailwind CSS + shadcn/ui (components only — no other component library)
- Backend: Supabase
  - Auth: Supabase Auth (email + password)
  - Database: PostgreSQL via Supabase
  - Storage: none
  - Edge Functions: no
- Additional packages: react-hook-form, zod

## Design System
- Component library: shadcn/ui
- Color palette: shadcn/ui default
- Typography: shadcn/ui default (Inter)
- Tone: professional, minimal
- Dark mode: no

## Scope — Build exactly these features
1. Email + password login screen (Supabase Auth)
2. Protected dashboard listing open tickets (title, status, created_at, assigned_to)
3. Create ticket form (title, description, priority: low / medium / high)
4. Ticket detail page with status update dropdown
5. Top navigation bar with logout button

## Out of v1 — Do not build
- Agent-to-agent ticket assignment
- Email notifications
- Analytics or reporting dashboard
- Customer-facing portal
- File attachments

## Security Constraints
- Authentication: required — Supabase Auth (email + password)
- Row-level security: tickets table — agents read/update own tickets; admins read all
- Input validation: zod on all forms (login, create ticket)
- Sensitive data: none beyond email in auth.users (Supabase-managed)

## DO NOT
- DO NOT add any feature not listed in Scope.
- DO NOT use any component library other than shadcn/ui.
- DO NOT generate placeholder content, lorem ipsum, or stub data.
- DO NOT add analytics, telemetry, or tracking scripts.
- DO NOT install packages not listed in the Stack section.
- DO NOT add a user registration flow — accounts are created by the admin in Supabase directly.
```

**Note to user (in their language):** Cole isso diretamente no prompt do novo projeto do Lovable. Se o Lovable fizer perguntas de acompanhamento, confirme apenas o que já está neste prompt — não expanda o escopo.

## Out of Scope

This skill does NOT handle:
- General product strategy or feature roadmap → discuss in conversation
- Lovable bug fixing or feature iteration after initial build → continue in Lovable chat
- Non-Lovable frontend projects (Cursor, Bolt, raw Vite setup) → write the prompt manually
- Mobile apps (React Native, Flutter) → not Lovable's output target

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "The user described the app in their message — I can skip discovery and write the prompt" | A description answers maybe 2 of the 6 questions. Missing stack, security, and design system specs produce a prompt Lovable fills with guesses — wrong libraries, wrong auth model, no RLS. |
| "The user is writing in Portuguese, so I'll write the prompt in Portuguese" | The output prompt is always in English. Lovable produces more robust code from English inputs. Tell the user this; write in English regardless of the conversation language. |
| "The design system section is optional when the user says 'default is fine'" | "Default" must still be written out explicitly. Without it, Lovable may introduce a different component library or ignore Tailwind. "shadcn/ui default" is a valid value — omitting the section is not. |
| "I'll mention extra constraints in the chat after delivering the prompt" | DO NOT rules only work if they are inside the Lovable prompt. Post-prompt chat instructions are ignored by Lovable. All constraints must go in Step 2. |
| "The 'Out of v1' section is optional for simple apps" | Without explicit exclusions, Lovable guesses what to build next and adds features. At least 1 exclusion is required even for the simplest apps. |
| "Security is only relevant for apps with sensitive data" | Security Constraints governs Supabase RLS and input validation for every database app, not just PII-heavy ones. Omitting it means Lovable skips RLS and adds no validation. |

## Before Marking Complete

- [ ] Step 1 complete — all 6 discovery questions answered or explicitly waived
- [ ] Prompt is in English
- [ ] All 7 sections present, none empty without justification
- [ ] At least 1 exclusion in "Out of v1"
- [ ] At least 5 DO NOT rules present
- [ ] Prompt delivered in a code block ready to paste
- [ ] 1-sentence usage note added in user's language after the code block

## After Completing: Log Learning

Append to `references/learnings.md`:

```
Date: [today]
App type: [internal tool / SaaS / B2C / etc.]
Discovery gaps: [which of the 6 questions the user struggled to answer]
Scope creep risk: [features the user almost added to v1]
What worked: [specific rule or section that prevented a problem]
What didn't: [anything that needed extra clarification]
```
