# Limites e vieses — o que o dado não diz

Ler antes de escrever qualquer conclusão. Cada item aqui já custou caro a alguém.

## 1. Fluxo de passantes não existe

Nem no dump, nem no produto. O score do Órbita tem 4 dimensões e nenhuma é
fluxo (`docs/confluence/ia/analises/estudo-peso-populacao-score-viabilidade.md`).
O indicador "fluxo estimado de comércios no entorno" discutido na spec modular é
**contagem de POI**, não fluxo.

Consequência: **rua comercial com poucos moradores é subestimada** — o caso 25
de Março. Potencial de consumo compensa em parte e **não é equivalente**.

→ Em ponto de perfil comercial, isto entra como **Dificuldade declarada**.
Nunca compensar com outro número e seguir.

## 2. O parecer histórico não prediz desfecho

Medido em `C:\Users\zequi\projetos\analise-ponto-orbita`:
- aprovado × reprovado: log-rank **p = 0,8275**, 101 fechamentos — curvas sobrepostas;
- contra o próprio brick, as reprovadas **não ficaram atrás**;
- porte do mercado local × faturamento da loja: **r = −0,003** (p = 0,97).

Dá para descartar efeito grande; não dá para descartar efeito pequeno (3–5 p.p.).

→ Vizinhança histórica é **memória**, não prognóstico.

## 3. Viés de seleção nas reprovadas

Só se observa ponto reprovado que **abriu** — aquele em que alguém teve
convicção para contrariar o parecer. Reprovado abandonado não tem desfecho.
"Reprovadas vão bem" **não** prova que a análise erra.

## 4. Dois fenômenos no mesmo status "Reprovado"

41 contratos abriram no endereço exato reprovado, em 40 endereços distintos.
Parte é **governança** (parecer contrariado), parte é **processo** (a análise
nunca rodou, o ponto já estava comprado). Os dois caem no mesmo status e
contaminam qualquer estatística.

## 5. Rateio dentro do setor censitário

**Resolvido, com uma premissa residual.** O rateio proporcional está
implementado: cada setor entra pela **fração da área dele que cai dentro do
círculo**, calculada por recorte geométrico do polígono.

A coerência foi verificada em Aracaju, raio de 300 m:

| Método | População | Densidade implícita | Densidade declarada | Erro |
|---|---|---|---|---|
| Setor inteiro | 1.416 | 5.008 hab/km² | 1.105 hab/km² | **+353%** |
| **Rateio por área** | **355** | **1.254 hab/km²** | 1.259 hab/km² | **−0,4%** |

Somar o setor inteiro produzia um número que **contradizia a densidade da
própria base**. O rateio bate dentro do viés de escala conhecido do cálculo de
área (+0,401% constante, por convenção de raio da Terra).

**O que resta como premissa:** a população se distribui uniformemente dentro de
cada setor. Num setor meio vazio e meio verticalizado isso erra. O refinamento é
o rateio **dasimétrico**, ponderado por área construída, que o acervo não tem.

**Taxa não se rateia.** Renda média, densidade e percentuais entram como média
ponderada — por população, por domicílios ou por área dentro do raio, conforme o
que a taxa descreve. Multiplicar uma taxa pela fração é o erro clássico do
rateio areal.

## 6. A UTC não é o raio

UTC e brick são unidades da CloseUp/IQVIA, não a área de influência da loja.
Em município com uma única UTC, o número é da cidade inteira. Em São Paulo
(84 UTCs) o dump não diz em qual o ponto cai.

## 7. A base da IQVIA é a carteira atual

O histórico foi retroagido: quem saiu da rede foi apagado para trás. Qualquer
recorte de loja fechada é não-mensurável nessa base.

## 8. Bases internas conflitam

Loja Farmarcas aparece dentro da camada `Concorrentes`
(`evolucao-camadas/orbita-evolucao-camadas.md:12`). `farmacias` vem da Receita
e não tem coordenada. CNES tem CNPJ e coordenada mas até ~15 dias de defasagem.

→ Divergência vira **item do dossiê**, com os dois números. Nunca escolher um
em silêncio.

## 9. Dado mensal da IQVIA é ruidoso

36 de 182 lojas oscilam mais de 5× entre o maior e o menor mês. **Nunca média
simples** — mediana e proporção.

## 10. O dump envelhece em silêncio

Extraído em 2026-10-26, sem rotina de atualização. Um dossiê de daqui a seis
meses parecerá igualmente preciso e não será. Carimbo de data é obrigatório.

## 11. O cadastro de lojas erra, e o zoneamento depende dele

- Só **1.841 das 2.804 lojas (66%)** têm coordenada utilizável: **931 estão
  vazias** e **32 caem fora do Brasil**. No terço restante não há como checar
  distância mínima — lacuna, não ausência de risco.
  *(Cuidado: "1.873" é o total de coordenadas preenchidas, válidas ou não.
  Preenchida e utilizável são contagens diferentes.)*
- Loja cadastrada em **Patrocínio Paulista/SP** tem coordenada a **342 m do
  centro de Franca/SP**. Como o teto é contado por cidade cadastrada, cadastro
  errado erra o teto junto.
- Bandeira Farmarcas dentro da camada Concorrentes **não prova** que a loja é
  nossa: "FCIA FARMAVALE" a 112 m do centro de Franca não existe no cadastro.

## 12. As duas leituras do teto de zoneamento discordam na prática

A regra aplicada conta **lojas**; a página 4.5 escreve **empresários**. Medido
sobre 830 cidades com loja ativa e código IBGE resolvido:

| Leitura | Cidades acima do teto |
|---|---|
| contando lojas | **207 (25%)** |
| contando empresários distintos | **34 (4%)** |

Passos/MG tem 7 lojas de **um único** empresário, com teto 2. Ou a regra é
rotineiramente dispensada, ou ela conta empresários, ou há um terceiro
critério não documentado. O script aplica a leitura por lojas e **mostra as
duas** sempre que elas discordam.

## 13. LGPD

`all_expansion.analysis_data` e `contratos_expansao` têm nome e e-mail de
empresários, consultores e analistas. Os scripts descartam esses campos; o
dossiê nunca os reproduz, nem citando parecer histórico.
