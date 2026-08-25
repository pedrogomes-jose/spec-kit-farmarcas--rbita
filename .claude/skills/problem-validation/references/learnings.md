# Aprendizados — problem-validation

Data: 2026-07-12
Modo: standalone
Problema validado: Vendedores de campo não preenchem o campo "próxima ação" no CRM porque preencher pelo celular seria lento demais.
O que funcionou: ancorar cada pergunta do roteiro em "última vez" / "última semana" força resposta factual e evita que o entrevistado dê opinião sobre a UI.
O que não funcionou: nada a reescrever nesta rodada — nenhuma pergunta gerada precisou de correção para sair do padrão opinião/desejo futuro.
Edge case: a causa assumida pelo usuário (lentidão no celular) é apenas uma de várias explicações plausíveis (falta de valor percebido, falta de cobrança do gestor, conectividade em campo) — o roteiro precisou deixar espaço pra essas emergirem sem sugeri-las.

Data: 2026-07-12
Modo: encadeado
Problema validado: RH confere manualmente mesmo com validação automática disponível (fechamento de folha, oportunidade priorizada vinda do /product-discovery).
O que funcionou: amarrar cada pergunta do roteiro a um fechamento nomeado ("o último fechamento", "a última vez que baixou a planilha") mantém a resposta em fato verificável mesmo quando o contexto herdado já vem carregado de uma causa-raiz assumida.
O que não funcionou: nada precisou de reescrita nesta rodada.
Edge case: a Suposição herdada do discovery (falta de confiança/transparência) já vinha marcada como evidência fraca na CSD — isso exigiu levantar 2 hipóteses alternativas no Passo 1 (exigência de compliance/auditoria; cobertura parcial da validação), não apenas 1, para não aceitar a causa-raiz herdada como dado só porque veio de uma sessão de discovery anterior.

Data: 2026-07-12
Modo: encadeado
Problema validado: RH confere manualmente mesmo com validação automática disponível (fechamento de folha, oportunidade priorizada vinda do /product-discovery) — rodada 2, testando a regra nova do bloco Critical sobre desafiar Suposição herdada com o mesmo rigor de uma nova.
O que funcionou: desmembrar a Suposição herdada composta ("falta de confiança/transparência") em duas causas distintas com soluções diferentes (confiança na acurácia vs. transparência sobre o escopo do que foi validado) deixou explícito que aceitar a suposição como veio do discovery já seria pular uma etapa de análise, não só de pergunta.
O que não funcionou: nada precisou de reescrita nesta rodada.
Edge case: a Suposição herdada já era, ela mesma, uma hipótese "mais sofisticada" que a causa ingênua original (falta de validação técnica) — isso criou risco de tratá-la como já validada por ser "melhor" que a hipótese anterior. O Passo 1 precisou nomear explicitamente que ela também é Suposição (não Certeza) e oferecer uma 3ª hipótese (responsabilização/exposição a risco pessoal) que nem a causa ingênua nem a Suposição herdada cobriam.
