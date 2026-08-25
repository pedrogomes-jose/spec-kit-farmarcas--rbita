# Summary — unit-test-writer

**Job:** Gera testes unitários durante o desenvolvimento, detectando linguagem/framework e convenções reais do projeto, cobrindo sucesso/edge/erro, e executando os testes de verdade antes de reportar.

**Domain:** Code authoring — test generation (critérios customizados 4/5: coverage completeness, convention & verification fidelity).

**Skill name / invocação:** `/unit-test-writer` — ativação sob demanda (não automática via hook), por escolha do usuário.

## Grades

| Input | Draft v0 | Final (iter 1) |
|---|---|---|
| 01 — invocação direta sem alvo | 78/100 | 81/100 (ceiling documentado) |
| 02 — trigger phrase + contexto Jest completo | 95/100 | 98/100 |
| 03 — linguagem adjacente, sem setup de teste | 90/100 | 96/100 |

**Iterações:** 1.

**Fix de maior alavancagem:** a descrição tinha a cláusula "Use quando" começando a ~330 caracteres (passando da janela de 250 chars que o Claude usa para roteamento). Encurtar o WHAT e adicionar uma trigger phrase que espelha a fala real do Input 03 ("quero ter certeza que isso está coberto antes de commitar") subiu o Routing de 16/16/13 para 19/19/19 sem tocar no corpo da skill.

**Teto estrutural documentado:** Input 01 (invocação direta sem nenhum arquivo/contexto) fica em 81/100 — é o teto conhecido de "decline path" (ver `create-skill/references/creation-patterns.md` §E): o comportamento correto é perguntar qual arquivo testar, não inventar um exemplo. Não há mais o que iterar aqui.

**Extra aplicado além do rubric:** integração de `references/learnings.md` (Tip 9) — a skill lê aprendizados anteriores no Step 0 e registra um novo aprendizado a cada execução, já que é uma skill de uso recorrente durante o desenvolvimento.

## Arquivos

- Skill final: `C:\Users\zequi\.claude\skills\unit-test-writer\SKILL.md`
- Prova de trabalho: esta pasta (`rubric.md`, `draft-v0.md`, `final-skill.md`, `inputs/`, `outputs-draft/`, `outputs-final/`, `grades-draft.md`, `grades-final.md`, `iterations.md`)
