# Rubric — software-improvement — 2026-06-30

Domain: Code authoring / multi-step provisioning (improvement PRD → investigate → clarify → implement)
Domain criteria chosen:
  4. Clarification completeness — ambiguidades identificadas nas 3 categorias (negócio, UX, técnicas) antes de implementar?
  5. Implementation gate enforcement — a Fase 2 foi bloqueada até as respostas chegarem? Nenhum código escrito prematuramente?

## Criteria (0–20 each, /100 total)

| # | Criterion | 0 | 10 | 14-18 | 20 |
|---|-----------|---|----|----|---|
| 1 | **Routing quality** | Skill não dispara em prompts relevantes | Dispara em alguns, falha em natural language | Dispara consistentemente; boundary bloqueia out-of-scope | Dispara em ≥9/10 casos relevantes; 3+ trigger phrases; "Do NOT use for" com pointers |
| 2 | **Output specificity** | Output genérico sem contexto do projeto | Usa algum contexto mas inventa detalhes | Principled-decline correto OU output usa dados reais do PRD + código | Output referencia arquivos, endpoints, tabelas e regras reais do projeto |
| 3 | **Output format consistency** | Shape diferente a cada execução | Shape parcialmente consistente | Template seguido com pequenas variações | Fase 1 e Fase 2 produzem shapes idênticos ao template |
| 4 | **Clarification completeness** | Nenhuma pergunta feita; implementa direto | Perguntas genéricas não baseadas no PRD ou código | Perguntas categorizadas mas incompletas — alguma categoria faltando | Todas as ambiguidades reais cobertas nas 3 categorias; perguntas com contexto ("O PRD diz X mas o código faz Y") |
| 5 | **Implementation gate enforcement** | Implementa código antes das respostas | Menciona dúvidas mas continua implementando | Aguarda na maioria dos casos; pequenos deslizes | Nenhum código escrito na Fase 1; Fase 2 claramente separada e iniciada somente após respostas |

## A+ threshold: ≥ 90/100 total, all inputs

## Principled-decline anchor
Quando o input não tem PRD, a resposta correta é exibir o decline determinístico do Step 0 (mensagem estruturada com o que incluir no PRD + preview do que a skill fará). Score:
- Routing: 18/20 (skill disparou corretamente)
- Specificity: 16-18/20 (decline é informativo, não vazio)
- Format: 18/20 (template do decline é consistente)
- Clarification completeness: 16/20 (sem PRD, não há como gerar perguntas — correto parar)
- Gate enforcement: 18/20 (não implementou — correto)
→ Total esperado no principled-decline path: ~86-90/100
