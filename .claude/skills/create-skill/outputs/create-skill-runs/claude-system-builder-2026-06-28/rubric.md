# Rubric — claude-system-builder

## Criteria (5 total, 20 pts each = 100 pts)

---

### C1 — Routing Quality (20 pts)

**What it measures:** Does the skill fire on the right inputs? Does it NOT fire on out-of-scope inputs? Is the trigger reliable for Portuguese and English natural-language requests?

| Score | Anchor |
|-------|--------|
| 20 | Skill fires on all 10+ trigger phrases; out-of-scope requests (Lovable app, agent flow) are correctly routed away before generating any spec |
| 16–18 | Fires on most triggers; one or two natural-language variants might be missed |
| 10–14 | Fires on explicit command but misses adjacent natural-language requests |
| 0–8 | Requires exact command; does not fire on conversational phrasing |

---

### C2 — Discovery Completeness (20 pts)

**What it measures:** Are all 7 discovery questions asked in a single message? Is the opening message deterministic (same shape every run)? Does it preview what the output will contain?

| Score | Anchor |
|-------|--------|
| 20 | All 7 questions in one message, fixed template used, "what you'll get" preview names all 8 sections, no dripping |
| 16–18 | 6–7 questions in one message, preview present but generic or slightly variable |
| 10–14 | Questions split across multiple messages, or fewer than 6 asked |
| 0–8 | No discovery phase; jumps directly to spec or asks questions one at a time |

---

### C3 — Output Format Compliance (20 pts)

**What it measures:** Are all 8 sections present? Are they in the correct order? Do implementation phases include the required 3 sub-elements (what builds, out of phase, acceptance criteria)? Is output in the user's language?

| Score | Anchor |
|-------|--------|
| 20 | All 8 sections present and in order, every phase has all 3 sub-elements, output matches user's language, no omitted sections |
| 16–18 | 7–8 sections present, phases mostly well-structured, minor format deviations |
| 10–14 | Some sections missing or phases lack acceptance criteria |
| 0–8 | Spec structure is freeform with no adherence to the 8-section template |

---

### C4 — Architecture Completeness (20 pts) [PRIMARY]

**What it measures:** Are tech stack, components, data models, integrations, and security constraints all specified and internally consistent? Do `[DEFAULT]` markers appear on inferred values? Are data models specific enough for Claude Code to infer the schema?

| Score | Anchor |
|-------|--------|
| 20 | All 5 architectural dimensions covered, data models have fields/types/relationships, integrations list auth method + operation, `[DEFAULT]` markers on all inferred values, zero silent guesses |
| 16–18 | 4–5 dimensions covered, most data models specified, a few unmarked defaults present |
| 10–14 | 3 dimensions covered, data models vague (entity names without fields), unmarked defaults throughout |
| 0–8 | Generic spec that could apply to any system; no specifics anchored to user's actual system |

---

### C5 — Implementation Sequencing (20 pts) [SECONDARY]

**What it measures:** Are phases numbered and named? Does each phase have explicit "out of this phase" items preventing scope creep? Are acceptance criteria concrete and verifiable? Do DO NOT rules cover the most dangerous failure modes for this specific system?

| Score | Anchor |
|-------|--------|
| 20 | 2–4 phases, each with explicit "out of this phase" list, acceptance criteria are commands (`curl`, `npm run`, observable state), DO NOT rules cover auth bypass + secrets + SQL injection + type safety + scope creep |
| 16–18 | Phases well-structured, acceptance criteria present but some vague, DO NOT rules cover most failure modes |
| 10–14 | Phases listed but "out of" items vague or absent, acceptance criteria are subjective ("tests pass") |
| 0–8 | Phases are a flat list with no scope boundaries, no acceptance criteria, generic DO NOT rules |

---

## Aggregate scoring

| Grade | Score |
|-------|-------|
| A+ | 90–100 |
| A  | 80–89 |
| B  | 70–79 |
| F  | <70 |

**A+ required on all 3 inputs before marking done.**
