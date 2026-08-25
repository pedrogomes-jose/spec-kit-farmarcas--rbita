# Learnings — user-stories skill runs

Log entries appended here after each real use. Format:

Date: [YYYY-MM-DD]
What worked: [specific pattern that produced good output]
What didn't: [what failed or needed correction]
Edge case: [anything unexpected]

---

Date: 2026-07-13
What worked: Splitting the PRD by layer (API/Backend, App/Frontend, Notificações) produced 8 clean, independently testable stories from 6 PRD requirements. Grouping "pedido cancelado" + "já avaliado" + "não entregue" validation rules into a single [API] Validar Elegibilidade story (multiple Gherkin ACs) avoided over-fragmenting a small, cohesive rule set.
What didn't: N/A — no Linear/Jira MCP was connected, confirmed via ToolSearch before falling back to markdown, per skill instructions.
Edge case: PRD stated a 7-day cutoff for the push notification but was silent on whether manual rating via order history ever expires. Flagged this explicitly as an ambiguity inside the story (not a contradiction — no conflicting requirement existed) rather than inventing a cutoff, and asked to confirm with product.

---

Date: 2026-07-13
What worked: Adjacent-language routing — input never said "user story"/"história de usuário", just "quebra isso em itens pro time começar a implementar essa semana" (PT-BR feature description with no PRD attached). This matched the skill's trigger phrase "quebra essa feature em histórias" closely enough to fire. The verbal description was already detailed enough (persona implied, action, default-filter rule, scale edge case, technical constraint) to treat as Caso A-equivalent and skip straight to generation instead of prompting the user for more info.
What didn't: The user's request for "uma lib compatível [com Cloudflare Workers]" is a technical spike with no direct user value — did not force it into a Gherkin user story (would have violated INVEST "Valiosa" from a user's perspective); instead surfaced it as a flagged Observação recommending a separate tech-spike ticket or /claude-system-builder, per the skill's Out of Scope list.
Edge case: ">500 transações → paginar" was split into its own story instead of folded in as an AC of the main export story, because it has an independent trigger condition and is independently testable — folding it in would have made the main story's Gherkin cover two unrelated behaviors under one Dado/Quando/Então pair.

---

Date: 2026-07-13
What worked: Re-running the same "Avaliação de Pedidos" PRD produced the same 8-story, layer-grouped breakdown (API/Backend, Notificações, App/Frontend) as a prior run logged above — confirms the split is stable, not an artifact of one pass. Also applied the Critical section's rule strictly to Prioridade, not just Estimativa: since priority was not given by the user or PRD, every story's Prioridade field got a `[DEFAULT: Px — confirmar com o time]` marker, even though the skill's own Worked Example only shows the marker on Estimativa. Critical-section text overrides an under-specified worked example.
What didn't: N/A — outputs/user-stories/avaliacao-de-pedidos-stories.md already existed from a prior run; overwrote it with a freshly-generated (independently reasoned, not copy-pasted) version rather than treating the pre-existing file as "already done" and skipping the task.
Edge case: Flagged one inferred (not literal-PRD) Gherkin AC — that the 30-minute push should be suppressed if the order was already rated before the timer fires — as an inference combining requisitos 1 and 3, distinct from the PRD-sourced ACs, so engineering knows to confirm rather than treat it as a literal PRD line.
