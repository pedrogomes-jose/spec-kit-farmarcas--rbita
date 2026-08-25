---
name: voice-brief
description: Transcreve áudio via Whisper (OpenAI), estrutura o transcript sem inventar conteúdo, e SEMPRE pergunta pra qual skill rotear o resultado — nunca decide sozinho. Use quando o usuário disser 'transcreve esse áudio', 'transforma esse áudio em texto', 'processa essa gravação', 'manda esse áudio pro discovery', 'gravei uma ideia, organiza isso', ou fornecer um caminho de arquivo de áudio (mp3/m4a/wav/ogg) pedindo para processá-lo. Do NOT use para decidir sozinho o próximo passo → sempre pergunte o destino; do NOT use para gravar áudio → forneça o arquivo já gravado; do NOT use para escrever o conteúdo final (PRD/discovery/histórias/decisões) → isso é feito pela skill escolhida (/product-discovery, /claude-system-builder, /problem-validation, /user-stories, /build-decisions, /lovable-prompt).
---

# voice-brief

Transcreve um arquivo de áudio via API do Whisper, limpa o transcript preservando fielmente o que foi dito, e pergunta ao usuário para qual skill encaminhar o conteúdo. Existe para substituir digitação de PRDs, discovery, histórias e decisões por gravação de voz — sem nunca inventar o que não foi dito, e sem nunca decidir sozinho o próximo passo.

## Critical

- **Nunca decidir sozinho pra qual skill rotear.** SEMPRE pergunte ao usuário (Step 4), mesmo quando o conteúdo do áudio parecer obviamente destinado a um tipo de skill específico.
- **Nunca inventar conteúdo que não foi dito no áudio.** Na limpeza (Step 3), remova apenas ruído de fala (hesitação, repetição, falso começo). Uma lacuna real vira `[TRECHO POUCO CLARO: verificar]`, nunca um preenchimento por suposição.
- **Parar se `OPENAI_API_KEY` não estiver configurada, ou se o arquivo de áudio não existir.** Nunca simular ou inventar uma transcrição para "seguir em frente".
- **Sempre salvar o transcript bruto em `outputs/voice-brief/` antes de qualquer limpeza.** O usuário precisa poder conferir a versão limpa contra o texto bruto retornado pela API.

## Step 0: Read Before You Write

| Source | Path | What to extract |
|--------|------|------------------|
| Arquivo de áudio | caminho fornecido pelo usuário na conversa | Existência do arquivo e extensão (mp3/m4a/wav/ogg/webm/mp4 — formatos aceitos pela API do Whisper) |
| Chave de API | variável de ambiente `OPENAI_API_KEY` | Presença da chave — sem ela, a skill para antes de tentar transcrever |
| Skills-irmãs disponíveis | `~/.claude/skills/*/SKILL.md` (e a pasta `.claude/skills/` do projeto atual, se existir) | Nome + descrição de cada skill, para oferecer como opção real de roteamento no Step 4 — nunca ofereça uma skill que não existe |
| Aprendizados passados | `references/learnings.md` | Padrões de formato de áudio ou destino que causaram problema em rodadas anteriores |

Se `references/learnings.md` não existir, prossiga sem ele.

## Step 1: Verificar Pré-Requisitos

Antes de qualquer chamada de API, confirme os dois itens abaixo. Não prossiga para o Step 2 sem os dois confirmados:

1. **Arquivo existe:** o caminho de áudio fornecido resolve para um arquivo real. Se não existir, pare e peça o caminho correto — não tente adivinhar o arquivo certo.
2. **Chave configurada:** `OPENAI_API_KEY` está definida no ambiente. Se não estiver, pare e explique como configurar (`export OPENAI_API_KEY=sk-...` no perfil do shell, ou o equivalente no SO do usuário) — nunca tente transcrever de outra forma nem simule o resultado.

Se qualquer um dos dois falhar, produza a saída da **Fase 1** do Worked Example abaixo e pare — não prossiga para o Step 2.

## Step 2: Transcrever via API do Whisper

Execute:

```bash
curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@<caminho-do-audio>" \
  -F model="whisper-1" \
  -F response_format="text"
```

Salve a resposta **exatamente como retornada pela API, sem edição**, em `outputs/voice-brief/<nome-do-audio>-transcript-bruto-<data>.md`, com uma linha de cabeçalho citando o arquivo de áudio original e a data.

Se a chamada retornar erro (chave inválida, arquivo acima de 25MB, formato não suportado), mostre o erro exato ao usuário e pare. Nunca gere um transcript fictício para seguir em frente.

## Step 3: Limpar e Estruturar (sem inventar)

A partir do transcript bruto salvo, produza uma versão organizada:

- Remova apenas ruído de fala: hesitações ("é... tipo... então"), repetições literais, falsos começos.
- Organize em tópicos/blocos coerentes se o áudio cobrir mais de um assunto — mantendo a ordem e o conteúdo do que foi dito.
- Nunca complete uma frase incompleta ou uma ideia que ficou vaga no áudio. Se algo não ficou claro, marque com `[TRECHO POUCO CLARO: verificar]` e siga.
- Nunca adicione conclusões, números ou fatos que não foram ditos no áudio.

Mostre a versão limpa **por completo na conversa** — não apenas o caminho do arquivo salvo.

## Step 4: Perguntar o Destino (roteamento sempre manual)

Depois de mostrar o transcript limpo, pergunte explicitamente para qual skill rotear. Liste como opções apenas skills verificadas no Step 0 — adapte a lista ao que estiver realmente instalado no ambiente atual. Use este formato:

> "Transcrição pronta. Pra onde eu levo isso?
> 1. **Discovery de produto** (`/product-discovery`) — mapear dores e oportunidades
> 2. **Validar uma hipótese específica** (`/problem-validation`) — JTBD + Mom Test
> 3. **Spec de sistema** (`/claude-system-builder`) — construir com Claude Code
> 4. **Prompt pro Lovable** (`/lovable-prompt`) — construir um app
> 5. **Histórias de usuário** (`/user-stories`) — quebrar em backlog
> 6. **Documentar decisões** (`/build-decisions`) — registrar regras/decisões já tomadas
> 7. **Nenhuma — só quero o transcript**
>
> Qual dessas (ou outra coisa)?"

## Step 5: Encaminhar com Contexto

Depois que o usuário escolher, invoque a skill escolhida passando o transcript limpo como contexto de entrada — não peça para o usuário colar o texto de novo. Se o usuário escolher "nenhuma", encerre confirmando apenas onde o transcript ficou salvo.

## Formato de Output

Sempre nesta ordem: (1) confirmação dos pré-requisitos, (2) transcript bruto salvo, (3) transcript limpo mostrado por completo na conversa, (4) pergunta de roteamento no formato numerado do Step 4, (5) após a resposta do usuário: encaminhamento com contexto ou encerramento.

## Worked Example

**Fase 1 — pré-requisito ausente:**

Input: "Transcreve esse áudio: C:\Users\pedro\Downloads\ideia-produto.m4a"

Output:
> "Não encontrei a variável `OPENAI_API_KEY` no ambiente — preciso dela pra chamar a API do Whisper. Configure com `export OPENAI_API_KEY=sk-...` (ou o equivalente no seu perfil de shell) e me chame de novo. O arquivo `ideia-produto.m4a` existe e está pronto pra transcrever assim que a chave estiver configurada."

**Fase 2 — fluxo completo (pré-requisitos OK):**

Input: "Transcreve esse áudio: C:\Users\pedro\Downloads\ideia-produto.m4a"

Output:
> "✅ Arquivo encontrado, `OPENAI_API_KEY` configurada. Transcrevendo...
>
> 📄 Transcript bruto salvo em `outputs/voice-brief/ideia-produto-transcript-bruto-2026-07-24.md`
>
> **Transcript organizado:**
> Ideia: um app que ajuda times de vendas a registrar a próxima ação direto pelo celular. Hoje ninguém preenche isso no CRM porque é lento — isso apareceu em pelo menos 3 conversas com vendedores essa semana. `[TRECHO POUCO CLARO: verificar]` a parte sobre integração com WhatsApp.
>
> Transcrição pronta. Pra onde eu levo isso?
> 1. **Discovery de produto** (`/product-discovery`)
> 2. **Validar uma hipótese específica** (`/problem-validation`)
> 3. **Spec de sistema** (`/claude-system-builder`)
> 4. **Prompt pro Lovable** (`/lovable-prompt`)
> 5. **Histórias de usuário** (`/user-stories`)
> 6. **Documentar decisões** (`/build-decisions`)
> 7. **Nenhuma — só quero o transcript**
>
> Qual dessas (ou outra coisa)?"

## Out of Scope

Esta skill NÃO faz:
- Gravar áudio → forneça o arquivo já gravado
- Decidir sozinho pra qual skill rotear → sempre pergunta (ver Critical)
- Escrever o PRD/discovery/histórias/decisões em si → isso é feito pela skill de destino escolhida: `/product-discovery`, `/claude-system-builder`, `/problem-validation`, `/user-stories`, `/build-decisions`, `/lovable-prompt`
- Transcrever sem `OPENAI_API_KEY` configurada → pare e peça a configuração

## Cross-Skill Routing

- Destino "Discovery de produto" → `/product-discovery`
- Destino "Validar hipótese" → `/problem-validation`
- Destino "Spec de sistema" → `/claude-system-builder`
- Destino "Prompt Lovable" → `/lovable-prompt`
- Destino "Histórias de usuário" → `/user-stories`
- Destino "Documentar decisões" → `/build-decisions`

## Common Shortcuts — Do Not Take These

| O que Claude pode pensar | Por que está errado |
|---|---|
| "O áudio claramente é uma ideia de produto nova, vou já rotear pro /product-discovery sem perguntar" | Roteamento é sempre manual — mesmo um conteúdo óbvio pode ter um destino diferente do esperado (ex: o usuário só queria guardar o transcript). Pular a pergunta do Step 4 quebra a regra central desta skill. |
| "A chave da API não está configurada, mas posso simular uma transcrição plausível baseada no nome do arquivo" | Isso é fabricação. Sem a chave, a skill para e pede a configuração — nunca inventa conteúdo de áudio que não foi processado. |
| "O trecho ficou confuso, vou completar com o que provavelmente foi dito" | Preencher lacunas é inventar conteúdo. Marque como `[TRECHO POUCO CLARO: verificar]` e siga — nunca complete por suposição. |
| "Vou só mostrar o caminho do arquivo salvo, sem colar o transcript limpo na conversa" | O usuário precisa ver o conteúdo completo pra decidir o roteamento no Step 4 — um caminho de arquivo sozinho não é suficiente pra essa decisão. |
| "Vou oferecer todas as skills que conheço, mesmo sem confirmar que existem nesse ambiente" | Uma opção de roteamento pra uma skill que não existe quebra no Step 5. Sempre liste apenas o que foi verificado no Step 0. |

## Before Marking Complete

- [ ] Step 0/1: arquivo de áudio e `OPENAI_API_KEY` verificados antes de qualquer chamada de API
- [ ] Transcript bruto salvo em `outputs/voice-brief/` antes da limpeza
- [ ] Transcript limpo mostrado por completo na conversa (não só o caminho do arquivo)
- [ ] Nenhuma lacuna preenchida por suposição — marcada com `[TRECHO POUCO CLARO: verificar]` quando aplicável
- [ ] Pergunta de roteamento feita explicitamente, com opções verificadas contra as skills realmente instaladas
- [ ] Nenhuma invocação de skill de destino ocorreu sem a escolha explícita do usuário
- [ ] Se o usuário escolheu um destino, o transcript foi passado como contexto sem pedir para colar de novo

## After Completing: Log Learning

Adicione ao final de `references/learnings.md`:

```
Data: [hoje]
Formato de áudio: [mp3/m4a/wav/outro]
Skill de destino escolhida: [nome ou "nenhuma"]
O que funcionou: [padrão de limpeza ou pergunta que funcionou bem]
O que não funcionou: [algo que precisou correção]
Edge case: [algo inesperado — áudio multilíngue, trecho inaudível, etc.]
```
