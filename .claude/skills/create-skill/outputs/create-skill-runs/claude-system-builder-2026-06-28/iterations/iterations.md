# Iteration Log — claude-system-builder

## Iteration 1

**Trigger:** Input 01 scored 85/100 (below 90 threshold). Lowest criterion: C5 Implementation sequencing (13/20).

**Root cause analysis:**

The opening discovery message previewed "Fases de implementação" as a section name without revealing its internal structure. A user seeing this preview knows a section called "Implementation Phases" will exist, but has no signal that:
1. Phases will be numbered and named after milestones
2. Each phase will explicitly list what stays OUT of that phase (scope guard)
3. Each phase will end with concrete, verifiable acceptance criteria

Without this expectation, Claude has weaker anchoring on the 3-sub-element phase structure when writing the spec. The phase granularity was also unspecified — the skill could produce 2 phases or 8, each ranging from 1 hour to 2 weeks of work.

Secondary finding: C4 Architecture completeness also low (15/20) because the preview listed sections sequentially without connecting Q3 (components) → sections 3+4, or Q7 (scope) → phase 1 boundary. The discovery session's architectural coverage was strong (7 questions, all dimensions) but the mapping wasn't visible.

**Fix applied:**

1. **Opening message preview** — changed from:
   > "A spec final terá 8 seções (Visão geral, Stack, Componentes, Modelos de dados, Contratos de integração, Segurança, Fases de implementação, Regras DO NOT)"

   To:
   > "A spec final terá 8 seções: Visão geral, Stack, Componentes, Modelos de dados, Contratos de integração, Segurança, **Fases de implementação** (cada fase lista o que construir, o que fica explicitamente fora e critérios de aceite verificáveis), e Regras DO NOT"

2. **Step 2 phase granularity note** — added after "Never leave a section thin or empty":
   > "Generate 2–4 phases. Each phase represents approximately 1–2 days of Claude Code implementation work. If a phase would span more than 3 days, split it. Name each phase after the logical milestone it achieves."

**Risk of regression:** None. Both changes are additive. No existing instruction was removed or modified. The changes only add information — to the preview (Change 1) and to Step 2 (Change 2). Inputs 02 and 03 can only benefit from tighter phase scoping.

**Score after iter-1:**

| Input | Before | After | Delta |
|-------|--------|-------|-------|
| 01 | 85 | 91 | +6 |
| 02 | 90 | 93 | +3 |
| 03 | 95 | 97 | +2 |
| Avg | 90.0 | 93.7 | +3.7 |

All inputs now ≥ 90. Iteration complete.

---

## What was NOT iterated

**C2 Discovery completeness (19/20 on Input 01):** -1 because the preview lists sections sequentially rather than mapping questions to sections. A further improvement (a numbered mapping table like "Q3 → sections 3 and 4") would push this to 20/20 but was judged marginal vs. the iter-1 fix. Deferred.

**C3 Output format compliance ceiling for Input 01:** The skill's correct behavior for no-context invocation is to ask questions — not to generate a spec. This inherently caps C3 at 18/20 for Input 01. Recognized as a structural ceiling; not iterated.

**Queue storage decision in Input 03:** The spec surfaces Bull+Redis as [DEFAULT] with pg-boss as alternative. A stronger recommendation would improve C4. Judged as out of scope for this skill — the skill's job is to surface the decision with options, not to make infrastructure choices for the user.
