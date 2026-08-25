# Summary — prd-router creation run

**Data:** 2026-06-28
**Skill:** prd-router
**Path:** C:\Users\zequi\.claude\skills\prd-router\SKILL.md
**Domain:** Decision (PRD routing — Lovable vs Software/Claude Code)

## Grades

| Input | Draft | Final | Delta |
|-------|-------|-------|-------|
| 01 (sem PRD) | 90 (A+) | 90 (A+) | 0 |
| 02 (HabitTrack — Lovable) | 98 (A+) | 98 (A+) | 0 |
| 03 (NotifyHub — Software) | 98 (A+) | 98 (A+) | 0 |
| **Avg** | **95.3** | **95.3** | 0 |

## Iterations: 0

Draft v0 convergiu em A+ direto. Stop condition met na primeira rodada.

## O que moveu o score no v0

1. **Tabela de classificação obrigatória com 5 critérios + evidências rastreáveis** — a regra "toda célula precisa citar o PRD ou 'não mencionado'" foi o principal driver de C2 e C4 para 20/20 em Inputs 02 e 03.

2. **"Argumento mais forte para o outro caminho"** — seção derivada do domínio Decision (kill criteria + anti-strawman). Os agentes produziram argumentos genuínos (risco de streak com timezones no HabitTrack; dashboard admin isolável no NotifyHub) — não strawman.

3. **Worked example com Phase 1 + Phase 2 inline** — elevou Input 01 de ~88 para 90. Precedente: investor-update (slot 25). Sem o worked example da Phase 2, C4 e C5 ficariam em 16/14, totalizando 88 (A-).

4. **Confirmação obrigatória antes de ativar skill** — NEVER rules no ## Critical baniram a ativação implícita. Nenhum agente tentou pular essa etapa.

5. **5 trigger phrases em PT + EN** — "analisa esse PRD" (Input 02) e "preciso saber se esse produto vai para o Lovable ou para o Claude Code" (Input 03) são formas naturais que o usuário brasileiro tiparia — não terminologia técnica.

## Teto estrutural Input 01

C2: 16/20 (principled-decline — sem PRD, sem especificidade)
C4: 18/20 (Phase 2 visível via worked example, não via output direto)
C5: 16/20 (kill criteria estrutura visível via Phase 2 do worked example)
Teto: 90/100 — correto, não é deficiência da skill.
