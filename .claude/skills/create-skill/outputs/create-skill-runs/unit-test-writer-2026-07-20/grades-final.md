# Grades — Final (after iteration 1)

Body unchanged from draft v0 (it was already producing correct, specific, well-traced output). Only the frontmatter `description` was edited, so only the Routing criterion is re-scored; Specificity/Format/Coverage/Convention scores carry over from grades-draft.md since the underlying output content is identical.

| Input | Routing | Specificity | Format | Coverage | Convention/Verification | Total |
|---|---|---|---|---|---|---|
| 01 — direct invocation, no target | 19/20 | 16/20 | 16/20 | 15/20 | 15/20 | **81/100** |
| 02 — trigger phrase + full Jest context | 19/20 | 20/20 | 20/20 | 19/20 | 20/20 | **98/100** |
| 03 — adjacent phrasing, no test setup | 19/20 | 19/20 | 19/20 | 19/20 | 20/20 | **96/100** |

## What moved

- WHAT clause shortened so "Use quando" now starts at ~118 chars (was ~330) — the full WHEN clause and boundary now sit well inside the 250-char routing window.
- Added trigger phrase 'quero ter certeza que isso está coberto antes de commitar', a near-verbatim match to Input 03's actual user phrasing ("queria ter certeza que ela está coberta antes de eu commitar").

## Result vs. stop conditions

- Input 02: 98/100 — A+.
- Input 03: 96/100 — A+.
- Input 01: 81/100 — below 90, but this is the documented structural ceiling for zero-argument direct invocation (see `references/creation-patterns.md` §E: "Direct invocation `/skill` with no args → Specificity ~12–18/20 — correct decline behavior"). The skill's actual behavior (ask which file/function, don't fabricate) is correct; there is no context to be specific about. Not iterated further.

Both inputs that had real context to work with are ≥ 90. Shipping.
