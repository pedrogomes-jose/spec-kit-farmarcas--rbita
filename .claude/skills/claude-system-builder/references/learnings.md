# Learnings — claude-system-builder

---

Date: 2026-06-28
Input type: creation-run (initial skill build)
What worked: Discovery message template with explicit phase-structure preview. Opening message that names "Fases de implementação (cada fase lista o que construir, o que fica explicitamente fora e critérios de aceite verificáveis)" sets user and Claude on the right expectations before any answers are received. Phase granularity note (2–4 phases, ~1–2 days each) prevents unbounded phases.
What didn't: Initial draft preview listed 8 section names sequentially without describing the internal structure of the most complex section (implementation phases). This left C5 Implementation sequencing at 13/20 on no-context inputs. Fix: parenthetical in the preview.
Edge case: Queue library selection (Bull vs. pg-boss vs. custom) is a real architectural decision that depends on whether Redis is available. The skill correctly surfaces it as [DEFAULT] but a stronger recommendation pattern (always ask Q5 follow-up for queue-based systems: "Does Redis exist in your infra?") would improve architecture completeness for worker-heavy systems.
