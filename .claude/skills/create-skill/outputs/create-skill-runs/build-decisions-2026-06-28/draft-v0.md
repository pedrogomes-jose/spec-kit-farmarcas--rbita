---
name: build-decisions
description: Extrai e documenta regras de negócio, decisões técnicas, constraints de escopo e guardrails de um prompt do Lovable ou spec de sistema já gerados na conversa, criando tabelas estruturadas no Miro (primário) ou em markdown (fallback). Use quando o usuário disser 'documenta as decisões', 'registra as regras de negócio', 'cria o doc de decisões', 'documenta o que foi criado', 'registra as decisões técnicas', 'ADR do projeto', 'quero documentar esse prompt', 'salva as decisões no Miro', 'document the decisions', ou após criar um artefato com /lovable-prompt ou /claude-system-builder. Do NOT use para criar prompts de Lovable → use /lovable-prompt; do NOT use para criar specs de sistema → use /claude-system-builder; do NOT use para discovery de produto → use /product-discovery; do NOT use para criar agentes → use /claude-agent-flow.
---

# build-decisions

Extrai regras de negócio, decisões técnicas, decisões de escopo e guardrails de um prompt do Lovable ou spec de sistema gerados na conversa, estrutura em três tabelas e cria no Miro. Funciona como o registro permanente de "por que isso foi decidido assim" — a memória do build.

## Critical

- **Fonte sempre é o artefato, nunca o modelo.** Nenhuma regra ou decisão pode ser inventada. Tudo deve ter origem em uma seção do prompt do Lovable ou da spec de sistema. Se a razão por trás de uma decisão não estiver explícita no artefato, marque como `[RACIONAL: não documentado]` e pergunte ao usuário.
- **Separação obrigatória entre regras e decisões.** Regra de negócio = o que o sistema deve ou não deve fazer do ponto de vista do negócio/usuário. Decisão técnica = escolha de tecnologia, arquitetura ou implementação com seu porquê.
- **Output vai para o Miro.** Crie três tabelas e um doc sumário no Miro. Se o Miro MCP não estiver disponível, entregue em markdown na conversa com aviso.
- **Não reescreva o artefato.** O output são decisões EXTRAÍDAS, não uma reformulação do prompt ou da spec.

## Step 0: Localizar Artefato e Preparar Miro

| Fonte | Onde | O que extrair |
|-------|------|---------------|
| Prompt do Lovable | conversa (seções: Context, Stack, Design System, Scope, Out of v1, Security, DO NOT) | Todas as seções |
| Spec de sistema | conversa (seções: System overview, Tech stack, Components, Data models, Security, Phases, DO NOT) | Todas as seções |
| Contexto Miro ativo | `mcp__claude_ai_Miro__context_get` | Board ativo para usar ou criar |
| Aprendizados | references/learnings.md | Padrões anteriores |

**Identificar artefato:**
- Se houver prompt do Lovable E spec de sistema na conversa → pergunte qual documentar (ou ambos).
- Se houver apenas um → prossiga sem perguntar.
- Se não houver nenhum → informe: *"Não encontrei nenhum prompt do Lovable ou spec de sistema na conversa. Crie um com /lovable-prompt ou /claude-system-builder, ou cole o artefato aqui."*

**Verificação Miro:** Use ToolSearch com `"select:mcp__claude_ai_Miro__context_get,mcp__claude_ai_Miro__board_create,mcp__claude_ai_Miro__table_create,mcp__claude_ai_Miro__doc_create"` antes de chamar qualquer ferramenta Miro.

Se `references/learnings.md` não existir, prossiga sem ele.

## Step 1: Enriquecimento Opcional de Racional

Após localizar o artefato, pergunte em uma única mensagem:

> "Antes de documentar, há justificativas por trás de alguma decisão que não estão explícitas no artefato? Por exemplo: por que esse backend e não outro? Por que algum item ficou fora do v1? Se não houver nada a adicionar, pode responder 'não' e eu documento o que está no artefato."

Se o usuário responder "não" ou não tiver adições → avance para o Step 2.
Se trouxer contexto → incorpore como `[RACIONAL: fornecido pelo usuário]` nas tabelas.

## Step 2: Extrair e Classificar

Percorra o artefato seção por seção e classifique cada item em uma das três categorias:

### Tabela 1 — Regras de Negócio
Items extraídos de: Security Constraints, DO NOT rules (perspectiva de negócio), Out of v1, políticas de acesso (ex: "agents can only read their own tickets").

| Regra | Categoria | Racional | Seção de origem |
|-------|-----------|----------|-----------------|
| [regra] | auth / dados / acesso / escopo / UX | [racional ou `[RACIONAL: não documentado]`] | [seção do artefato] |

### Tabela 2 — Decisões Técnicas
Items extraídos de: Stack, Additional packages, Design System, Tech stack, Components, Data models, DO NOT rules (perspectiva técnica).

| Decisão | Racional | Alternativa implícita | Seção de origem |
|---------|----------|----------------------|-----------------|
| [decisão] | [racional ou `[RACIONAL: não documentado]`] | [alternativa descartada, se inferível] | [seção do artefato] |

### Tabela 3 — Escopo e Guardrails
Items extraídos de: Scope, Out of v1, Implementation phases, DO NOT rules (perspectiva de escopo).

| Item | Status | Motivo | Seção de origem |
|------|--------|--------|-----------------|
| [item] | ✅ v1 / ❌ fora do v1 / 🚫 nunca | [motivo ou `[RACIONAL: não documentado]`] | [seção do artefato] |

## Step 3: Criar no Miro

Execute na ordem:

**3.1 — Board:** Chame `mcp__claude_ai_Miro__context_get`. Se não houver board ativo, chame `mcp__claude_ai_Miro__board_create` com nome `"Decisões de Build — [nome do projeto] — [data]"`.

**3.2 — Tabela de Regras de Negócio:** Chame `mcp__claude_ai_Miro__table_create` com:
- Título: `📋 Regras de Negócio — [nome do projeto]`
- Colunas: `Regra`, `Categoria`, `Racional`, `Seção de origem`
- Linhas: uma por item da Tabela 1

**3.3 — Tabela de Decisões Técnicas:** Chame `mcp__claude_ai_Miro__table_create` com:
- Título: `⚙️ Decisões Técnicas — [nome do projeto]`
- Colunas: `Decisão`, `Racional`, `Alternativa implícita`, `Seção de origem`
- Linhas: uma por item da Tabela 2

**3.4 — Tabela de Escopo e Guardrails:** Chame `mcp__claude_ai_Miro__table_create` com:
- Título: `🗺️ Escopo e Guardrails — [nome do projeto]`
- Colunas: `Item`, `Status`, `Motivo`, `Seção de origem`
- Linhas: uma por item da Tabela 3

**3.5 — Doc sumário:** Chame `mcp__claude_ai_Miro__doc_create` com:
- Título: `📌 Sumário de Decisões — [nome do projeto]`
- Conteúdo:
  ```
  Artefato de origem: [Prompt Lovable / Spec de Sistema] — [data]
  Total de regras de negócio: [N]
  Total de decisões técnicas: [N]
  Total de itens de escopo/guardrails: [N]
  Itens com racional não documentado: [N] — revisar com o time
  ```

**3.6 — Confirmar na conversa:**
> "Documentação criada no Miro ✓
> - 📋 [N] regras de negócio
> - ⚙️ [N] decisões técnicas
> - 🗺️ [N] itens de escopo e guardrails
> - [N] itens marcados como `[RACIONAL: não documentado]` — considere revisar com o time
>
> [Nome do board]"

## Fallback Markdown (Miro indisponível)

Se qualquer chamada Miro falhar, entregue em markdown na conversa:

```markdown
## 📋 Regras de Negócio — [projeto]

| Regra | Categoria | Racional | Seção de origem |
|-------|-----------|----------|-----------------|
| ...   | ...       | ...      | ...             |

## ⚙️ Decisões Técnicas — [projeto]

| Decisão | Racional | Alternativa implícita | Seção de origem |
|---------|----------|----------------------|-----------------|
| ...     | ...      | ...                  | ...             |

## 🗺️ Escopo e Guardrails — [projeto]

| Item | Status | Motivo | Seção de origem |
|------|--------|--------|-----------------|
| ...  | ...    | ...    | ...             |
```

E avise: *"Miro não está conectado. Cole o markdown acima no seu documento ou conecte o Miro MCP e rode novamente."*

## Exemplo Trabalhado

**Artefato de origem (Prompt Lovable — app de suporte CS):**
```
## Stack
- Framework: React + TypeScript + Vite
- Styling: Tailwind CSS + shadcn/ui
- Backend: Supabase (Auth: email + password; Database: PostgreSQL)
- Additional packages: react-hook-form, zod

## Security Constraints
- Authentication: required — Supabase Auth (email + password)
- Row-level security: tickets table — agents read/update own tickets; admins read all
- Input validation: zod on all forms

## DO NOT
- DO NOT add a user registration flow — accounts created by admin in Supabase directly.
- DO NOT add analytics or tracking scripts.
```

**Tabela 2 extraída (Decisões Técnicas):**

| Decisão | Racional | Alternativa implícita | Seção de origem |
|---------|----------|----------------------|-----------------|
| Supabase Auth (email + password) | Stack já é Supabase — auth nativo | Clerk, Auth0 | Stack |
| react-hook-form + zod | Validação tipada em formulários | Formik, validação manual | Stack / Additional packages |
| shadcn/ui como única component library | Consistência visual, sem conflito de estilos | MUI, Chakra | Stack / DO NOT |

**Tabela 1 extraída (Regras de Negócio):**

| Regra | Categoria | Racional | Seção de origem |
|-------|-----------|----------|-----------------|
| Agents só leem/editam próprios tickets | acesso | Isolamento de dados entre agentes | Security Constraints |
| Admins leem todos os tickets | acesso | Supervisão por papel | Security Constraints |
| Sem auto-cadastro — admin cria contas | auth | `[RACIONAL: não documentado]` | DO NOT |
| Sem analytics ou tracking | escopo | `[RACIONAL: não documentado]` | DO NOT |

## Saídas Fora de Escopo

Esta skill NÃO lida com:
- Criar prompts de Lovable → use /lovable-prompt
- Criar specs de sistema → use /claude-system-builder
- Discovery de produto → use /product-discovery
- Criar agentes → use /claude-agent-flow

## Atalhos Comuns — Não Tome Estes

| O que Claude pode pensar | Por que está errado |
|--------------------------|---------------------|
| "Vou inferir o racional que não está no artefato" | Racional inventado é pior que ausente — o time vai confiar nele como se fosse uma decisão real. Marque como `[RACIONAL: não documentado]` e pergunte. |
| "Vou criar uma tabela única com tudo misturado" | Regras de negócio e decisões técnicas têm audiências diferentes. Misturar força o time a filtrar manualmente. Três tabelas separadas são obrigatórias. |
| "O artefato não tem seção de racional, então vou pular a pergunta do Step 1" | O Step 1 existe para capturar contexto que está na cabeça do usuário e não no artefato. Sempre pergunte, mesmo que o artefato pareça completo. |
| "Vou criar um único doc de texto no Miro com tudo" | Tabelas no Miro são editáveis e filtráveis. Docs de texto não são. Use `table_create` para as três tabelas e `doc_create` apenas para o sumário. |
| "Não há artefato na conversa — vou documentar o que o usuário descreveu verbalmente" | Documentar uma descrição verbal produz decisões imprecisas. Exija o artefato formal ou direcione para /lovable-prompt ou /claude-system-builder. |

## Antes de Marcar Completo

- [ ] Artefato localizado na conversa (Lovable prompt ou spec de sistema)
- [ ] Step 1 executado: enriquecimento perguntado ao usuário
- [ ] Tabela 1 (Regras de Negócio): ≥ 1 item por categoria relevante (auth / dados / acesso / escopo)
- [ ] Tabela 2 (Decisões Técnicas): toda escolha de stack, biblioteca e arquitetura documentada
- [ ] Tabela 3 (Escopo e Guardrails): todos os itens de Scope, Out of v1 e DO NOT mapeados
- [ ] Itens sem racional explícito marcados como `[RACIONAL: não documentado]`
- [ ] Nenhum item inventado — todos têm seção de origem identificada
- [ ] Step 3 executado: 3 tabelas + 1 doc sumário criados no Miro (ou fallback em markdown com aviso)

## Após Concluir: Registrar Aprendizado

Adicione ao final de `references/learnings.md`:

```
Data: [hoje]
Tipo de artefato: [Prompt Lovable / Spec de sistema / ambos]
Itens com racional não documentado: [N]
O que o Step 1 surfaceou de novo: [contexto que não estava no artefato]
O que funcionou: [padrão de extração que gerou boa separação]
O que não funcionou: [ambiguidade entre regra de negócio e decisão técnica]
```
