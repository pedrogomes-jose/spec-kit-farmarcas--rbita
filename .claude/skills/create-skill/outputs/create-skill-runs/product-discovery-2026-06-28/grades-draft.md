# Draft Grades (pre-iteration)

| Input | C1 Routing | C2 Specificity | C3 Format | C4 Discovery Depth | C5 Framework Accuracy | Total | Grade |
|-------|------------|----------------|-----------|--------------------|-----------------------|-------|-------|
| 01 (direto) | 20 | 16 | 17 | 16 | 16 | 85 | A |
| 02 (churn parcial) | 20 | 17 | 18 | 16 | 18 | 89 | A |
| 03 (contexto rico) | 20 | 19 | 20 | 19 | 19 | 97 | A+ |
| **Avg** | | | | | | **90.3** | **A+** |

**Inputs 01 e 02 abaixo de 90.** Problemas:
- Input 01: sem template de abertura determinístico (format 17), sem preview das 4 fases (discovery 16)
- Input 02: sem acknowledgment do contexto parcial antes de perguntar (format 18, discovery 16)
- Adicionalmente: Miro não integrado ainda (output era só texto)

**Fix aplicado:** (1) Template de abertura determinístico com preview das 4 fases + menção do Miro; (2) Instrução de contexto parcial ("Aqui está o que já entendi:"); (3) Fase D completamente reescrita com Miro integration (table_create, diagram_create, doc_create) + fallback em texto.
