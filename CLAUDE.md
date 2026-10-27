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

## Análise de região (dossiê de ponto)

Para avaliar uma região/endereço com dados, use a skill
`.claude/skills/analise-regiao-farmarcas/`. Ela roda sobre o dump local das
bases do Órbita em `C:\Users\zequi\Downloads\bases órbita` (sobrescreva com a
variável de ambiente `ORBITA_BASES`) e entrega um dossiê com forças,
fragilidades, oportunidades e dificuldades da região.

Regras que valem para qualquer análise de dado neste projeto:

- **Nenhum número sai do modelo.** Todo valor vem de um script determinístico
  ou de API pública consultada na sessão. Sem script de origem, não entra.
- **Fonte, arquivo e data do dump** acompanham cada número. O dump é estático
  e envelhece em silêncio.
- **Lacuna é declarada**, com o que a destravaria — nunca preenchida por
  estimativa.
- **O dossiê não pontua.** A régua de viabilidade 0–20 pertence ao produto e
  tem dono (executivos da Farmarcas). Duplicá-la cria dois números divergentes
  para a mesma pergunta.
- **Raio é a unidade de análise**, não isócrona — é o que o produto usa e o que
  torna o resultado comparável com a tela.
- **Nome de pessoa nunca entra** em entregável: as bases de análises e
  contratos contêm dados pessoais (LGPD).
- **Zoneamento é gate, não indicador.** Nenhuma análise de ponto segue sem
  passar pelas regras oficiais de expansão (Confluence 4.5 e 6.1). Se a regra
  barra, o entregável é o impedimento — não um estudo de mercado.
- **Perfil do solicitante é pergunta obrigatória**: empresário novo ou já
  associado. Loja Farmarcas vizinha é conflito entre associados num caso e
  escolha estratégica no outro.
- **"Loja nossa" é o que está no cadastro de lojas (CNPJ + coordenada)**, nunca
  o que casa por nome de bandeira na camada Concorrentes.
