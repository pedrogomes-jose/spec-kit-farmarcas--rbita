# Grades — Draft v0

| Input | Routing | Specificity | Format | Coverage | Convention/Verification | Total |
|---|---|---|---|---|---|---|
| 01 — direct invocation, no target | 16/20 | 16/20 | 16/20 | 15/20 | 15/20 | **78/100** |
| 02 — trigger phrase + full Jest context | 16/20 | 20/20 | 20/20 | 19/20 | 20/20 | **95/100** |
| 03 — adjacent phrasing, no test setup | 13/20 | 19/20 | 19/20 | 19/20 | 20/20 | **90/100** |

## Evidence

**Input 01** — correctly identified no target and asked which file/function, per Passo 1 and the Critical rule against inventing examples. Scored per the principled-decline anchor (structural ceiling for zero-arg invocation — see `references/creation-patterns.md` section E), not a skill defect.

**Input 02** — detected Jest from `package.json`, mirrored the exact existing convention (`__tests__` folder, `describe`/`it`, `expect().toBe()`), produced 8 well-distributed cases across success/edge/error, and traced each assertion by hand against the real function body instead of asserting a fabricated pass. Near-ceiling.

**Input 03** — correctly detected the absence of any test framework/convention and applied `[DEFAULT: ... — confirmar com o usuário]` to both the framework choice and the folder/naming convention, rather than silently picking pytest. Traced all 8 cases including a `None` → `TypeError` edge case. **Routing scored 13/20**: the user's phrasing ("queria ter certeza que ela está coberta antes de eu commitar") does not quote any of the 5 trigger phrases verbatim, and while the description's catch-all ("pedir cobertura de testes para uma função/classe/módulo específico") plausibly covers it, this is uncertain — a real router might treat it as a general dev question instead.

## Lowest-scoring criterion

**Routing quality**, driven by two compounding issues:
1. The description's WHAT clause ran ~330 characters before "Use quando" started — past the 250-char window Claude uses for routing (Tip 1 / audit item 4).
2. No trigger phrase covered the "coverage before commit" latent phrasing tested by Input 03.

This is the highest-leverage fix: shorten the WHAT clause and add a trigger phrase matching Input 03's actual wording.
