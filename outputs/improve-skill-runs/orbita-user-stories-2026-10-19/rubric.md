# Rubrica — orbita-user-stories (2026-10-19)

5 critérios × 20 pontos = /100. A+ = 90+. A = 80-89. B = 70-79. C = <70.

Domínio: autoria de card de backlog (ticket spec) para devs júnior, a partir de
PRD / estudo / transcrição de reunião, com destino no board Jira SQO.

---

## 1. Routing quality (description) — universal

| Faixa | Âncora |
|---|---|
| 18-20 | 100+ chars; WHAT+WHEN nos primeiros 250; 3+ frases que o usuário realmente digita; "Do NOT use for" COM ponteiro `→ use /X`; 3ª pessoa; cobre as fontes reais (PRD, estudo, transcrição) e o caso "atualizar card existente" |
| 14-17 | Tudo acima menos 1 item (ex.: não cobre transcrição como fonte, ou boundary sem ponteiro) |
| 10-13 | Dispara no caso óbvio mas perde o adjacente; boundary genérico |
| 5-9 | Sem boundary ou sem WHEN |
| 0-4 | Sem frontmatter / nome não bate com a pasta |

## 2. Output specificity — universal

| Faixa | Âncora |
|---|---|
| 18-20 | Card cita arquivo:linha / endpoint / componente REAL verificado na sessão, ou declara "Não localizado"/"Não aplicável" com o motivo; números e nomes vêm da fonte, não de suposição plausível |
| 14-17 | Específico mas 1-2 pistas não verificadas, OU declínio correto por falta de contexto que nomeia o que falta (ver âncora de declínio) |
| 10-13 | Mistura verificado e plausível sem distinguir |
| 5-9 | Genérico; caminho de código inventado por convenção |
| 0-4 | Nada específico; poderia ser de qualquer produto |

**Âncora de declínio com princípio:** input sem contexto (ex.: `/skill` sem args) cujo output correto é parar e nomear o que falta → specificity 14-18, não 4.

## 3. Output format consistency — universal

| Faixa | Âncora |
|---|---|
| 18-20 | Seções do template SQO na ordem exata, todas presentes (inclusive as vazias marcadas "Nenhum"/"Não informado"); 3 execuções dariam a mesma forma |
| 14-17 | Template seguido, 1 seção omitida quando vazia em vez de marcada |
| 10-13 | Ordem alterada ou seções fundidas |
| 5-9 | Formato próprio com pedaços do template |
| 0-4 | Formato reinventado (ex.: Como/Eu quero/Para que) |

## 4. Implementabilidade por júnior — DOMÍNIO (primário)

Um dev júnior sem contexto prévio consegue ler uma vez e começar?

| Faixa | Âncora |
|---|---|
| 18-20 | Todo termo de domínio definido em 1 frase; regras numeradas e atômicas (1 regra = 1 item verificável); declara explicitamente o que NÃO muda; Contexto traz comportamento atual + por que está errado + impacto de negócio; alternativas descartadas registradas com o motivo; pista de código verificada |
| 14-17 | Falta 1 dos itens (tipicamente "o que não muda" ou "alternativa descartada") |
| 10-13 | Regra em parágrafo corrido; "porquê" ausente; júnior precisaria perguntar 1-2 coisas |
| 5-9 | Jargão não definido; só o "o quê" |
| 0-4 | Card só faz sentido para quem já vive o domínio |

## 5. Honestidade sobre o que não se sabe — DOMÍNIO (secundário)

| Faixa | Âncora |
|---|---|
| 18-20 | Toda ambiguidade/contradição da fonte vira item explícito citando o trecho literal; "Nenhum" escrito quando não há; `[DEFAULT: X]` em todo valor não confirmado; campo herdado de template marcado para confirmar; efeito de segunda ordem fora da tela pedida declarado; porção lida da fonte declarada quando a leitura foi parcial |
| 14-17 | Faltou 1 (tipicamente efeito de segunda ordem ou herança de template) |
| 10-13 | Ambiguidade mencionada de passagem, sem citação da fonte |
| 5-9 | Ambiguidade resolvida em silêncio escolhendo uma interpretação |
| 0-4 | Regra inventada apresentada como decidida |
