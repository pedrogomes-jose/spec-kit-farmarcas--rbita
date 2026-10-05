# Rubric — orbita-user-stories

5 critérios, 20 pontos cada, /100 total. A+ = 90+, A = 80-89, B = 70-79, C = <70.

1. **Qualidade de roteamento (descrição)** — a descrição dispara nos prompts
   certos? 100+ chars, WHAT+WHEN nos primeiros 250 chars, 3+ frases-gatilho,
   fronteira "Do NOT use for" com ponteiro, terceira pessoa.
2. **Especificidade da saída** — o card usa contexto real (arquivo/endpoint
   confirmado nos 3 repositórios, número real do PRD) ou soa genérico?
3. **Consistência de formato** — três rodadas do mesmo input produzem a
   mesma forma (as 7 seções do template SQO, na mesma ordem)?
4. **[Domínio primário] Fidelidade ao template Jira SQO** — o card usa
   exatamente as 7 seções oficiais (Contexto, Referências visuais,
   Caminho/rota, Escopo do card, Regras de negócio, Critérios de aceite,
   Figma), na ordem certa, com os itens fixos de Critérios de aceite
   presentes?
5. **[Domínio secundário] Verificação de código real + revisão júnior** — toda
   pista de caminho/endpoint foi checada contra os 3 repositórios (não
   inventada), e o card só é apresentado como final com veredito "pronto
   para o júnior" do subagente `(?_?) revisor-clareza-junior`?

**Âncora de recusa fundamentada**: se o input não trouxer PRD/spec nem
descrição verbal, a saída correta é o template de Step 1 Caso B (parar e
pedir a fonte) — isso pontua 14-18/20 em especificidade e nos critérios de
domínio, não 0-4/20.
