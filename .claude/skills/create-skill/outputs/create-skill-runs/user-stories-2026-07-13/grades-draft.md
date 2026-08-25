# Grades — draft v0

## Input 01 (direct invocation, no PRD/spec — principled-decline path)

| Criterion | Score (/20) | Evidence |
|---|---|---|
| Routing quality | 20 | Direct `/user-stories` invocation, N/A for description-match but skill correctly loaded |
| Output specificity | 17 | Correct decline per Step 1 Caso B; checked every Step 0 source including ToolSearch for Linear/Jira before declining |
| Output format consistency | 18 | Decline template followed verbatim, checklist included |
| Acceptance-criteria completeness (domain) | 18 | No stories generated (correct); preview of Gherkin/INVEST accurately described |
| Traceability & default-marker discipline (domain) | 18 | Preview of traceability + `[DEFAULT]` behavior accurately described |
| **Total** | **91/100** | **A+** |

## Input 02 (PRD pasted inline, trigger phrase quoted, no MCP connected)

| Criterion | Score (/20) | Evidence |
|---|---|---|
| Routing quality | 20 | Quoted trigger phrase "quebra essa feature em histórias" |
| Output specificity | 20 | 8 stories, every one cites the exact PRD requirement number/text; flagged a real ambiguity (7-day cutoff vs. manual rating) instead of inventing an answer |
| Output format consistency | 13 | **Gap found**: final chat response was a *summary* + pointer to the saved markdown file, not the full story text — breaks from the worked example's inline-full-content pattern. Underlying file content (verified by reading it directly) was excellent and matched the template exactly. |
| Acceptance-criteria completeness (domain) | 20 | Every story has ≥2 Gherkin ACs incl. edge cases (empty comment, char limit, cancelled order, already-rated order, zero-review average, etc.); stories correctly split by layer (API/App/Notificações) |
| Traceability & default-marker discipline (domain) | 20 | Every story cites PRD requirement number; every estimate carries `[DEFAULT: X — confirmar com o time]`; ambiguity flagged explicitly inside the story rather than resolved silently |
| **Total** | **93/100** | **A+ overall, but format-consistency gap is real and cheap to fix** |

## Input 03 (adjacent natural language, no PRD, verbal feature description)

| Criterion | Score (/20) | Evidence |
|---|---|---|
| Routing quality | 18 | Correctly fired on latent trigger match ("quebra isso em itens pro time implementar") with no verbatim trigger phrase; reasoning was explicit and correct |
| Output specificity | 19 | Every story quotes the user's exact words; technical constraint (Cloudflare Workers, no client-side canvas) correctly kept out of the user-facing story and surfaced as an engineering note instead |
| Output format consistency | 19 | Full story text shown inline (title, As a/I want/So that, Gherkin AC ×2, rastreabilidade, estimativa, prioridade, dependências) + Tabela Resumo — matches template |
| Acceptance-criteria completeness (domain) | 19 | 2 ACs per story covering happy path + edge case; correctly split ">500 transações → paginar" into its own story (independent trigger condition) instead of overloading the main story's Gherkin |
| Traceability & default-marker discipline (domain) | 19 | Every story traces to the user's literal quote; DEFAULT markers present; correctly treated the "lib compatível com Cloudflare Workers" ask as an out-of-scope technical spike rather than forcing it into a user story (INVEST "Valiosa" reasoning) |
| **Total** | **94/100** | **A+** |

## Input 04 (out-of-scope: "write the PRD from scratch")

| Criterion | Score (/20) | Evidence |
|---|---|---|
| Routing quality | 20 | Correctly identified the request as PRD-writing, which the Out of Scope section explicitly excludes |
| Output specificity | 19 | Named the two correct routing targets (`/claude-system-builder` vs `/lovable-prompt`) with the actual decision criterion (system/backend vs. Lovable app) |
| Output format consistency | 19 | Matches the Out-of-Scope-decline shape used elsewhere in the skill family (prd-router, product-discovery) |
| Acceptance-criteria completeness (domain) | 18 | N/A — no stories; preview of what `/user-stories` will do once a PRD exists is accurate |
| Traceability & default-marker discipline (domain) | 18 | N/A — preview accurate |
| **Total** | **94/100 — PASS** | Correctly declined and routed, did not attempt to write a PRD or fabricate stories |

## Average (inputs 01–03)

(91 + 93 + 94) / 3 = **92.7/100 — all A+**

## Lowest-scoring criterion

Output format consistency on Input 02 (13/20) — the only real defect found. Root cause: the skill's Step 4 / Output Format did not explicitly require the full story text to appear in the chat response, only that it be saved/ticketed. Fixed in iteration 1: added a `## Critical` rule, an anti-rationalization table row, and an exit-checklist item requiring the full story text in the response regardless of where else it's persisted.
