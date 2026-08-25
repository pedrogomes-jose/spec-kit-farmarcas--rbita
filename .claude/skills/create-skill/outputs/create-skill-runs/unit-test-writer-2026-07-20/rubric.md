# Rubric — unit-test-writer

Domain: Code authoring (test generation) — não mapeada 1:1 na tabela padrão de domínios; critérios 4 e 5 customizados porque o job central do usuário tem dois eixos específicos: cobertura de casos (sucesso/edge/erro) e fidelidade à convenção real do projeto + execução verificada (nunca fabricada).

5 critérios, 0–20 cada, total /100. A+ = 90+.

1. **Routing quality (0–20)** — a descrição tem 100+ chars, WHAT+WHEN nos primeiros 250 chars, 3+ trigger phrases no estilo do usuário, boundary "Do NOT use for X → use /Y", terceira pessoa.
2. **Output specificity (0–20)** — usa contexto real (arquivo/função nomeados, framework realmente detectado, comando real) em vez de exemplo genérico de treino. Caminho de decline correto (sem alvo identificável) pontua 14–18, não perto de 0.
3. **Output format consistency (0–20)** — três execuções produziriam a mesma estrutura de output (o template com Framework/Convenção/Casos/Código/Execução)?
4. **Coverage completeness (0–20)** — os testes gerados cobrem sucesso, edge cases e erro explicitamente, ou declaram por que uma categoria não se aplica, em vez de omitir silenciosamente.
5. **Convention & verification fidelity (0–20)** — a skill detecta e segue a convenção real do projeto (ou marca `[DEFAULT: ... — confirmar]` quando não existe uma); e reporta uma execução real dos testes (comando + resultado), nunca um resultado presumido/fabricado.

Salvo em `outputs/create-skill-runs/unit-test-writer-2026-07-20/rubric.md`.
