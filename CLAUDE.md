# Órbita

## Contexto do produto

O Órbita é a ferramenta interna da Farmarcas usada pelo time de Expansão para
avaliar a viabilidade econômica de possíveis pontos comerciais para novas lojas.

Hoje, analistas coletam manualmente diversas "camadas" de dados vinculadas a uma
área geográfica (renda da população, faixa etária, concorrentes num raio de 500m
de um endereço, etc.) e, a partir dessas camadas, montam à mão um score do ponto
ou da região. Esse processo depende fortemente do conhecimento prévio de quem
analisa — saber quais camadas usar e o que é um bom ou mau resultado para cada
uma.

O produto deve assumir a coleta e a pré-análise dessas camadas, entregando um
primeiro resultado que já diga muito sobre o local e destacando para o analista
apenas os pontos que realmente exigem atenção humana. Isso torna o tempo do
analista mais estratégico e menos operacional. A expectativa de evolução do
produto é reduzir progressivamente tanto o conhecimento prévio quanto o número
de comandos/passos necessários para o analista chegar ao resultado da análise.

### Glossário do domínio

- **Área**: recorte geográfico (ex: bairro, raio ao redor de um endereço) usado
  como unidade de análise.
- **Camada**: uma fonte/tipo de informação coletada sobre uma área ou ponto
  (renda, faixa etária, concorrência, etc.).
- **Ponto (comercial)**: endereço/local candidato à abertura de uma nova loja.
- **Score**: avaliação consolidada da viabilidade de uma área ou ponto,
  hoje montada manualmente a partir das camadas.

## Estado atual do repositório

Repositório em estágio inicial — ainda sem código de produto. O que existe hoje:

- `.specify/` — estrutura do [spec-kit](https://github.com/github/spec-kit)
  (templates, constitution, scripts) usada para o fluxo spec-driven development.
- `.claude/skills/` — skills do spec-kit (`speckit-*`) mais skills pessoais de
  produto/discovery (`product-discovery`, `problem-validation`, `pm-especialista`,
  `claude-system-builder`, `lovable-prompt`, etc.).

## Fluxo de trabalho (spec-kit)

Novas features neste projeto devem seguir o fluxo spec-driven do spec-kit:

1. `/speckit-constitution` — define/atualiza princípios e regras de governança
   do projeto (ainda não executado).
2. `/speckit-specify` — cria a especificação de uma feature.
3. `/speckit-clarify` (opcional) — reduz ambiguidades antes do plano.
4. `/speckit-plan` — gera o plano de implementação.
5. `/speckit-tasks` — quebra o plano em tarefas executáveis.
6. `/speckit-analyze` (opcional) — checa consistência entre spec/plan/tasks.
7. `/speckit-implement` — executa a implementação.
