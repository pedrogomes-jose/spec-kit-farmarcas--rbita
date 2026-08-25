# Iterations Log — build-decisions

## Iteration 1

Input 01 (82) abaixo do threshold.

Root cause: decline message não mostrava o que seria extraído — "não encontrei artefato" genérico. Format 18, extraction 14, traceability 14.

Fix: decline determinístico em Step 0 com preview dos 3 nomes de tabela, colunas específicas (incluindo "Seção de origem"), e instruções de próximo passo para /lovable-prompt ou /claude-system-builder. Moveu:
- Format: 18→20 (template fixo)
- Extraction: 14→18 (preview do escopo completo de extração)
- Specificity: 16→17 (routing nomeado + estrutura de saída descrita)
- Traceability: 14→16 (menciona "Seção de origem" como coluna explícita)

Input 01: 82→91 (A+). Sem regressões. Stop.
