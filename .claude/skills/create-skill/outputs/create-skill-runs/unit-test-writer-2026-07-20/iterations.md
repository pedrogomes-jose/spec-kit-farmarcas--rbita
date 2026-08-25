# Iteration Log — unit-test-writer

## Iteration 1

**Trigger:** lowest-scoring criterion across the 3 draft inputs was Routing quality (16, 16, 13 /20), driven by:
1. Description WHAT clause ~330 chars before "Use quando" — past the 250-char routing window (Tip 1).
2. No trigger phrase matched Input 03's real phrasing ("queria ter certeza que ela está coberta antes de eu commitar").

**Fix applied:** rewrote the `description` field only (body untouched):
- Shortened the WHAT clause from ~330 to ~118 chars before "Use quando" begins.
- Added trigger phrase 'quero ter certeza que isso está coberto antes de commitar'.
- Moved the "cobre sucesso/edge/erro, executa de verdade" detail to after the trigger-phrase list (it doesn't need to be in the first 250 chars — it's a WHAT elaboration, not a routing signal).

**Result:** Routing 16→19, 16→19, 13→19 across the three inputs. Totals: 78→81 (Input 01, still capped by structural decline ceiling — expected, not a defect), 95→98 (Input 02), 90→96 (Input 03).

**Stop condition met:** the two inputs with real context to act on (02, 03) both score ≥ 90. Input 01's sub-90 score is the documented zero-arg-invocation ceiling from `references/creation-patterns.md` §E, not chased further.

No second iteration needed.
