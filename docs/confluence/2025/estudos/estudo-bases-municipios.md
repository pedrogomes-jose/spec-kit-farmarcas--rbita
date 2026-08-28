# Estudo sobre bases de municípios

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3270279170/Estudo+sobre+bases+de+munic+pios · Última atualização no Confluence: mai. 15, 2025
> Nota: esta página continha imagens no Confluence original que não puderam ser migradas automaticamente. Consulte a fonte acima para o conteúdo visual completo.

### ✅ **1. Identifique a origem dos dados**

| Nome da Base | Possível Origem ou Instituição | Possível API pública ou integração |
| --- | --- | --- |
| Densidade Demográfica MM | IBGE | Sim (IBGE API) |
| Domicílios Segundo Classe Econômica | IBGE / PNAD | Sim (IBGE ou dados PNAD contínua) |
| Empresas Totais / Segmentos | Receita Federal / RAIS / CNPJ | Sim, via Serpro (paga) ou Receita (limitada) |
| Firjan | Sistema FIRJAN | Provavelmente não tem API pública |
| Índice Educação | INEP / IBGE | Sim (INEP tem dados abertos, mas nem sempre via API) |
| PIB 2021 | IBGE | Sim |
| Pirâmide Etária / População | IBGE | Sim |
| Potencial de Consumo | IPC Maps / Geofusion / CNDL | Provavelmente apenas via contrato/licença (sem API aberta) |
| Movimentação Econômica | BACEN / Receita / IBGE | Sim, parcialmente |
| Ranking de Consumo | Empresas privadas (Nielsen, IPC) | Provavelmente só via contrato |

---

### 🔄 **2. Caminhos para Automação**

Você tem algumas possibilidades para automatizar essas cargas de dados:

#### a. **Integração via API (dados abertos)**

Para bases como IBGE, INEP, Receita e BACEN, você pode:

* Usar endpoints REST disponíveis.
* Criar um processo agendado (ex: via backend em Node, Python etc.) que consome esses dados e converte para o formato interno do Órbita.

#### b. **Integração com serviços pagos**

Ex: **CNPJ da Receita via Serpro**, dados demográficos de empresas como Geofusion, Neoway, etc.

#### c. **Robôs de raspagem (web scraping)**

Alternativa quando não há API pública. Pode ser usado para dados da FIRJAN, por exemplo.

---

### **3. Discutir com time técnico**

* Como será o agendamento de importações automáticas?
* Vai substituir ou complementar a importação manual por planilhas?
* Quais formatos de dados precisam ser tratados (CSV, JSON etc.)?

---

### 💡 Exemplo prático

Você quer automatizar a base **População MM 2023** (provavelmente do IBGE). Pode usar:

```
bash
```

CopiarEditar

`https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2023/variaveis/93?localidades=N1[all] `

Isso traz dados da população em 2023 por região.

---

### 🚀 Próximos passos sugeridos

1. Liste todas as bases + fonte de origem.
2. Verifique se tem API ou se é necessário contratar.
3. Envolva o time técnico para desenhar uma arquitetura de automação.
4. Defina um MVP: comece com 1 ou 2 bases simples (ex: população, PIB) para validar.
