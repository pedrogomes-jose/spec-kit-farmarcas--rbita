# Summary — /user-stories skill creation

**Spec:** Gera histórias de usuário em Gherkin (Dado/Quando/Então) com critérios de aceite, a partir de um PRD/spec existente ou de uma feature descrita verbalmente, criando tickets no Linear/Jira (se conectado) ou salvando em markdown.

**Domain classification:** Custom hybrid (closest precedent: `create-tickets` from `examples.md`). Primary criterion: acceptance-criteria completeness & INVEST compliance. Secondary: traceability to source + `[DEFAULT]`-marker discipline for unconfirmed estimates (borrowed from the "config-producing skills" pattern in `creation-patterns.md`, since story points/priority are exactly this kind of inferred value).

**Intake:** 4 fields confirmed with the user via AskUserQuestion (name, acceptance-criteria format, story source, output destination); trigger phrases and out-of-scope boundary were inferred from the verified sibling-skill set (`claude-system-builder`, `lovable-prompt`, `product-discovery`, `problem-validation`, `prd-router`, `build-decisions`) since the user's original request was a one-line request.

**Before/after:**
| | Input 01 (decline) | Input 02 (PRD pasted) | Input 03 (adjacent language) | Input 04 (out-of-scope) |
|---|---|---|---|---|
| Draft v0 | 91 (A+) | 93 (A+, but format 13/20) | 94 (A+) | 94 (PASS) |
| Final | 91 (A+) | 100 (A+) | 94 (A+) | 94 (PASS) |

**Average (inputs 01–03):** 92.7 → 95.0

**Iterations:** 1.

**Highest-leverage fix:** requiring the full story text to appear in the chat response, not just a summary + file pointer, when stories are saved to markdown instead of pushed to Linear/Jira. Added as a `## Critical` rule, an anti-rationalization table row, and an exit-checklist item. This closed a real inconsistency (Input 02 summarized, Input 03 showed full text) discovered only by reading the underlying saved file directly — the summary alone looked plausible.

**What didn't need fixing:** traceability, Gherkin/INVEST completeness, DEFAULT-marker discipline, and routing were all strong from the v0 draft, because the domain-specific defaults (traceability citation, `[DEFAULT: X — confirmar]` markers, contradiction-flagging) were baked in at draft time per `creation-patterns.md`'s config-producing-skill row, rather than discovered through iteration.

**Structural ceilings (not iterated against):** Input 01's principled-decline path caps specificity/format around 17-18/20 — correct behavior. Linear/Jira MCP connectivity could not be verified live in this environment (methodology gap, not a skill defect).

**Files:**
- Shipped skill: `C:\Users\zequi\.claude\skills\user-stories\SKILL.md`
- Learnings: `C:\Users\zequi\.claude\skills\user-stories\references\learnings.md`
- Proof of work: this folder (`rubric.md`, `draft-v0.md`, `final-skill.md`, `inputs/`, `grades-draft.md`, `grades-final.md`, `iterations.md`, `iterations/iter-1-skill.md`)
