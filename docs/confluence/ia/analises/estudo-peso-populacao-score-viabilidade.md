# Estudo do Peso de População no Score de Viabilidade

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/4159832069/Estudo+do+Peso+de+Popula+o+no+Score+de+Viabilidade · Última atualização no Confluence: jun. 16, 2026
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

# Resumo

‌

Ao informar um endereço e ajustar o **raio de análise**, o sistema exibe a **população na área (residentes)** com base na soma de habitantes dos **setores censitários** que intersectam o círculo desenhado no mapa. Esse valor vem da camada interna **Densidade Demográfica do Setor (hab/km²)**, não é inventado pela IA.

No **score de viabilidade**, a população é uma das **quatro dimensões** de pontuação, com peso máximo de **5 pontos em 20** (**25%** da escala total). Para **10.189 habitantes**, a faixa aplicável é **10.000–19.999**, resultando em **1 ponto** na dimensão população (**5%** do score máximo global).

A IA (Gemini) **não calcula** a população, ela recebe o número já agregado pelo backend e aplica as **regras de pontuação** definidas no prompt. Hoje **não existe** modelagem explícita de **fluxo de passantes** ou consumo não-residente, cenários como a **25 de Março** podem ser subestimados pela métrica de população residente.

---

# Objetivo do estudo

‌

Responder às seguintes questões:

1. De onde vem o valor **"População na área (residentes)"** ao alterar o raio?
2. Esse valor está alinhado com a camada **Densidade Demográfica do Setor (hab/km²)**?
3. **Qual peso** a população representa no cálculo de viabilidade?
4. **Como a IA utiliza** esse dado no score?
5. Seria possível, no futuro, **embasar áreas com poucos moradores e alto fluxo de passantes**?

---

# Cálculo de População em Função do Raio

‌

### Algoritmo

1. O frontend envia `lat`, `lng` e `radius` (metros) para `GET /layers/radius`.
2. O backend gera um **polígono circular** (Turf.js) representando a área de estudo.
3. Consulta setores censitários cujo polígono **intersecta** o círculo (`$geoIntersects` no MongoDB).
4. Para os setores encontrados, **soma** o campo `properties.Residentes` da camada **Densidade Demográfica do Setor (hab/km²)**.
5. O resultado é exposto como `summary.population`.

---

# Limitações Metodológicas

‌

Estas limitações não invalidam o dado da camada, mas explicam diferenças entre o que o analista enxerga no mapa e o número agregado.

| Limitação | Descrição | Impacto |
| --- | --- | --- |
| **Setor inteiro na conta** | Se o círculo corta apenas parte de um setor, soma-se a população **total** daquele setor, não a fração proporcional dentro do raio | Pode **superestimar** ou **subestimar** de acordo com o recorte |
| **População ≠ densidade × área do círculo** | `demographicDensity` é **média** da densidade dos setores, não `população / área do raio` | Duas métricas com significados distintos |
| **Residentes, não passantes** | A camada reflete **população residente** (IBGE/setor censitário) | Áreas comerciais com poucos moradores podem parecer "pequenas" |
| **Concorrentes fora do score** | `competitorsTotal` vem no `/layers/radius`, mas **não entra** no payload de `/analysis` | Saturação competitiva não pontua hoje |

---

# Peso de População no Score de Viabilidade

‌

### Modelo de pontuação (escala total: 20 pontos)

O score é composto por **4 dimensões**, cada uma valendo até **5 pontos**:

| # | Dimensão | Peso máximo | % do total |
| --- | --- | --- | --- |
| 1 | **População na área** | 5 pts | **25%** |
| 2 | Densidade demográfica | 5 pts | 25% |
| 3 | Potencial de consumo mensal (drogarias) | 5 pts | 25% |
| 4 | Classificação econômica (renda) | 5 pts | 25% |

### Faixas de pontuação — População

| Habitantes na área | Pontos (dimensão população) | % do score máximo (20) |
| --- | --- | --- |
| > 200.000 | 5 | 25% |
| 120.000 – 199.999 | 3 | 15% |
| 20.000 – 119.999 | 2 | 10% |
| **10.000 – 19.999** | **1** | **5%** |
| < 10.000 | 0 | 0% |

### Aplicação ao exemplo solicitado (10.189 habitantes)

| Métrica | Valor |
| --- | --- |
| População informada | 10.189 |
| Faixa aplicável | 10.000 – 19.999 |
| Pontos na dimensão população | **1 de 5** |
| Contribuição máxima possível no score total | **1 de 20 (5%)** |

> **Nota:** o score final depende também das outras três dimensões (densidade, consumo e renda). A população sozinha **não define** o resultado — ela contribui com **até 25%** do teto teórico.

### Faixas das demais dimensões (referência)

#### Densidade demográfica (hab/km²)

| Faixa | Classificação | Pontos |
| --- | --- | --- |
| ≤ 5.000 | Baixíssima | 5 |
| 5.001 – 10.000 | Baixa | 3 |
| 10.001 – 25.000 | Média | 2 |
| > 25.000 | Alta | 0 |

> **Atenção:** a lógica de densidade é **inversa** à de população — densidades **menores** pontuam **mais**.

#### Potencial de consumo mensal

| Faixa (R$) | Pontos |
| --- | --- |
| > 2.000.000 | 5 |
| 1.500.000 – 2.000.000 | 4 |
| 1.000.000 – 1.499.999 | 3 |
| 500.000 – 999.999 | 2 |
| < 500.000 | 1 |

#### Classificação econômica (renda média)

| Classe | Pontos |
| --- | --- |
| A++ / A+ (≥ R$ 19.024,01) | 0 |
| B1 / B2 (R$ 4.508,01 – 19.024) | 1 |
| C1 / C2 (R$ 1.275,01 – 4.508) | 3 |
| D / E (≤ R$ 1.275) | 5 |

### Classificação final do score

| Score (0–20) | Classificação | Perfil | Status (scorePercent ≥ 34) |
| --- | --- | --- | --- |
| 16 – 20 | Alta viabilidade | Excelente | Recomendado |
| 12 – 15 | Viabilidade moderada | Bom | Recomendado |
| 8 – 11 | Baixa viabilidade | Não recomendado | Recomendado |
| < 8 | Não recomendado | Ruim | Não Recomendado |

**Score percentual:** `(score / 20) × 100`, arredondado sem casas decimais.

---

# População vs densidade demográfica

‌

São **dimensões independentes** no score, com lógicas distintas:

| Métrica | O que representa | Como é calculada no summary | Lógica de score |
| --- | --- | --- | --- |
| **População** | Total de residentes na área | Soma de `Residentes` dos setores intersectados | **Mais habitantes → mais pontos** |
| **Densidade** | Concentração habitacional | Média de `Densidade Demográfica` dos setores | **Densidade menor → mais pontos** |

### Implicação prática

Uma área pode ter:

* **População moderada** (ex.: 10.189 → 1 pt) **e**
* **Densidade alta** (> 25.000 hab/km² → 0 pts na dimensão densidade)

Nesses casos, o score passa a depender mais fortemente de **potencial de consumo** e **renda**.

---

# Áreas com poucos moradores e alto fluxo (ex.: 25 de Março)

‌

### Situação atual

**Não há modelagem explícita** de:

* fluxo de passantes;
* visitantes diários;
* índice comercial de rua;
* horários de pico ou sazonalidade de consumo.

O sistema utiliza **população residente** e **potencial de consumo em drogarias por setor censitário**. O potencial de consumo pode **compensar parcialmente** população baixa, mas **não é equivalente** a fluxo de passantes.

### Por que 25 de Março é um caso especial

| Característica | Efeito no modelo atual |
| --- | --- |
| Poucos residentes no setor | População baixa → **poucos ou zero pontos** em população |
| Alto volume comercial diário | **Não capturado** diretamente |
| Consumo elevado de não-moradores | Pode aparecer **parcialmente** em `consumptionPotential` |
| Densidade residencial vs. fluxo comercial | Métricas de IBGE **não distinguem** "rua comercial" |

---

# Possibilidades Futuras

‌

| Abordagem | O que traria | Esforço | Prioridade sugerida |
| --- | --- | --- | --- |
| **Proxy via potencial de consumo** | Usar consumo alto + população baixa como sinal de mercado comercial | Baixo | Curto prazo (UX/explicabilidade) |
| **Breakdown visível no frontend** | Mostrar ao analista por que o score penalizou ou não a população | Baixo | Curto prazo |
| **Camada de fluxo / mobilidade** | Passantes estimados (operadoras, parceiros de dados) | Alto | Médio/longo prazo |
| **Índice comercial por POI** | Concentração de varejo (Google Places, OSM, bases internas) | Médio | Médio prazo |
| **Novo eixo no score: fluxo estimado** | 5ª dimensão ou peso híbrido em consumo | Médio–alto | Longo prazo |
| **Tipologia de mercado** | Flag `residential` / `mixed` / `commercial_high_traffic` com regras alternativas | Médio | Médio prazo |

---

# Proposta Conceitual de Tipologia

‌

---

# Recomendações e Backlog Sugerido

‌

### Curto prazo

* **Exibir breakdown de score na UI,** mostrando pontos por dimensão (população: 1/5, densidade: X/5, etc.).
* **Documentar na interface** que população é igual à soma de residentes dos setores que intersectam o raio.
* **Alinhar backend**, integrando cálculo determinístico (`scoring.ts`) ou expor breakdown na resposta de `/analysis`.
* **Tooltip ou help text** explicando diferença entre população residente e fluxo comercial.

### Médio prazo

* **Estudo comparativo**, comparando 25 de Março vs. bairro residencial: população, consumo, score e percepção do analista.
* **Regra de tipologia de mercado**, identificando cenários `commercial_high_traffic` via consumo + densidade + contexto urbano.
* **Incluir concorrentes no score ou na narrativa**, usando `competitorsTotal` já disponível no radius.

### Longo prazo

* **Camada ou parceiro de fluxo de passantes**, implementando footfall, mobilidade ou índice comercial.
* **Novo eixo ou peso híbrido**, compensando população baixa em centros comerciais.
* **Recorte proporcional por interseção**, ponderando população pela fração do setor dentro do raio (melhoria metodológica).

---

# Conclusão

‌

A **população na área** exibida ao ajustar o raio é um dado **confiável e determinístico**, originado da camada **Densidade Demográfica do Setor (hab/km²)** via soma de `Residentes` dos setores censitários intersectados. No score de viabilidade, ela representa **até 25% do teto teórico (5 de 20 pontos)**; para **10.189 habitantes**, a contribuição é de **1 ponto (5% do máximo global)**.

A IA **aplica** esse dado nas regras de pontuação, mas **não o calcula**. Para maior transparência ao analista, recomenda-se expor o **breakdown por dimensão** na API e na UI. Quanto a **áreas de alto fluxo com poucos residentes** (como a 25 de Março), o modelo atual **não captura passantes explicitamente**, o que seria uma evolução futura, com potencial de consumo como proxy imediato e camadas de fluxo como solução de médio/longo prazo.
