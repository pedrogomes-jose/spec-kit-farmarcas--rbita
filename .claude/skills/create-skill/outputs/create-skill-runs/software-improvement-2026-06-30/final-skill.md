---
name: software-improvement
description: Analisa um PRD de melhoria em projetos de software existentes, investiga o estado atual do código, gera perguntas de esclarecimento categorizadas (regras de negócio, UX/usabilidade, questões técnicas) e implementa SOMENTE após as dúvidas serem respondidas. Use quando o usuário disser 'tenho um PRD de melhoria', 'quero melhorar o app', 'implementar melhoria no projeto', 'aplicar esse PRD', 'melhorar o software', 'implementar as mudanças do PRD', 'fazer melhorias no sistema', 'preciso melhorar o projeto', 'aplique as melhorias', ou 'melhoria baseada em PRD'. Não use para criar projetos do zero → use /claude-system-builder. Não use para rotear PRD entre destinos → use /prd-router. Não use para debug ou code review sem PRD.
---

# software-improvement

Executa melhorias em projetos de software existentes a partir de um PRD. Lê o PRD, investiga o estado atual do código, identifica ambiguidades em três categorias (regras de negócio, UX/usabilidade, técnicas), aguarda respostas e só então implementa. A Fase 1 fecha as dúvidas; a Fase 2 escreve código. Nunca inverte essa ordem.

## Critical

- **Nunca implementar sem resolver dúvidas primeiro.** A Fase 2 começa somente após o usuário responder às perguntas da Fase 1. Não há exceção a essa regra.
- **PRD obrigatório antes de qualquer análise.** Se nenhum PRD for encontrado na conversa ou em arquivo, exibir o decline determinístico do Step 0 e parar.
- **Regras de negócio não são inferidas.** Qualquer decisão de produto não documentada explicitamente no PRD deve virar uma pergunta — nunca uma suposição silenciosa.
- **Escopo fechado.** Implementar apenas o que está no PRD. Não adicionar melhorias oportunistas não solicitadas.
- **Convenções do projeto prevalecem.** Usar a mesma linguagem, estilo de imports, nomenclatura e estrutura de arquivos do projeto existente.

## Step 0: Localizar PRD e Estado Atual do Projeto

| Fonte | Onde buscar | O que extrair |
|-------|-------------|---------------|
| PRD de melhoria | Conversa atual (texto colado) ou caminho de arquivo fornecido | Funcionalidades a adicionar/mudar/remover; restrições; critérios de aceite |
| Arquitetura atual | CLAUDE.md, README.md, wrangler.toml, package.json, tsconfig.json | Stack técnica, estrutura de pastas, dependências |
| Rotas e endpoints | Arquivos em routes/, api/, src/routes/ | Endpoints afetados pela melhoria |
| Modelos de dados | schema.ts, migrations/, *.sql | Tabelas e campos relevantes |
| Componentes de UI | pages/, components/, src/pages/ | Telas e componentes afetados |
| Learnings | references/learnings.md (se existir) | Padrões anteriores registrados |

**Se nenhum PRD for encontrado na conversa:**

> Não encontrei um PRD de melhoria na conversa. Para prosseguir, preciso de um documento descrevendo as mudanças desejadas.
>
> **O que incluir no PRD de melhoria:**
> - **Contexto:** qual problema ou oportunidade motiva essa melhoria?
> - **Funcionalidades:** o que deve ser adicionado, alterado ou removido?
> - **Regras de negócio:** quais regras específicas governam essa melhoria?
> - **Fluxo de UX:** como o usuário deve interagir com a nova funcionalidade?
> - **Restrições técnicas:** há limitações de performance, segurança ou compatibilidade?
> - **Critérios de aceite:** como saber que a melhoria foi implementada corretamente?
>
> Cole o PRD diretamente aqui ou forneça o caminho do arquivo. Após receber, farei:
> 1. Investigação do projeto atual (arquivos, rotas, schema)
> 2. Mapeamento de ambiguidades em 3 categorias
> 3. Perguntas de esclarecimento em uma única mensagem
> 4. Implementação somente após suas respostas

## Step 1: Analisar PRD contra Estado Atual

Com o PRD e os arquivos do projeto lidos, mapear:

1. **Funcionalidades afetadas:** quais rotas, componentes, tabelas e regras de negócio existentes a melhoria toca?
2. **Gaps de informação:** quais aspectos do PRD estão ambíguos, incompletos ou contraditórios com o código atual?
3. **Riscos técnicos:** mudanças de schema, breaking changes em APIs, impactos em fluxos existentes.
4. **Dependências de implementação:** existe código que precisa mudar antes da melhoria ser possível?

Organizar os gaps encontrados nas três categorias para o Step 2.

## Step 2: Apresentar Perguntas de Esclarecimento (Fase 1)

Apresentar TODAS as dúvidas em uma única mensagem, organizadas por categoria. Não implementar nada antes de receber as respostas.

```
## Perguntas antes de implementar — [nome da melhoria]

Analisei o PRD e o projeto. Antes de implementar, preciso esclarecer [N] pontos:

### Regras de Negócio
1. [pergunta com contexto: "O PRD menciona X, mas a regra atual é Y. Qual deve prevalecer?"]

### UX / Usabilidade
2. [pergunta sobre fluxo: "Quando o usuário fizer X, o sistema deve mostrar Y ou Z?"]
3. [pergunta sobre comportamento: "O feedback de sucesso deve ser inline ou toast?"]

### Técnicas
4. [pergunta técnica: "Devo criar uma nova tabela ou adicionar campos à existente?"]
5. [pergunta de compatibilidade: "A mudança em X vai afetar o endpoint Y já em uso?"]

Assim que você responder, implemento na ordem lógica.
```

Se o PRD for claro em alguma categoria e não houver dúvidas reais, omitir essa seção — não forçar perguntas onde não há ambiguidade genuína.

## Step 3: Aguardar Respostas (Gate Obrigatório)

PARAR aqui. Não avançar para a Fase 2 sem receber as respostas do Step 2.

Se o usuário liberar uma questão com "use seu julgamento" ou "como achar melhor", registrar a decisão assumida antes de implementar:

> "Assumindo [X] para a questão [Y], conforme sua instrução."

## Step 4: Implementar as Melhorias (Fase 2)

Com todas as dúvidas respondidas, implementar na seguinte ordem lógica:

1. **Migrations / schema** (mudanças no banco de dados)
2. **Backend** (rotas, lógica de negócio, validações, middleware)
3. **Frontend** (componentes, páginas, fluxos de UI)
4. **Configuração** (wrangler.toml, variáveis de ambiente, CORS, etc.)

Para cada arquivo:
- Ler o arquivo atual antes de editar
- Editar apenas o necessário para a melhoria — não refatorar código adjacente não relacionado
- Usar as mesmas convenções do projeto (linguagem, estilo, imports, nomenclatura)

## Output Format

**Fase 1 — Perguntas:**

```
## Perguntas antes de implementar — [nome da melhoria]

Analisei o PRD e o projeto ([arquivos lidos]). Encontrei [N] pontos que precisam de esclarecimento:

### Regras de Negócio
1. [pergunta específica]

### UX / Usabilidade
2. [pergunta específica]

### Técnicas
3. [pergunta específica]

Assim que você responder, implemento em sequência.
```

**Fase 2 — Implementação:**

```
Implementando com base nas suas respostas:

**[1/N] [Tipo]: [descrição do que foi feito]**
[ferramenta de edição aplicada]

**[2/N] [Tipo]: [descrição]**
[ferramenta de edição aplicada]

---
Implementação concluída. [N] arquivos editados.
Próximos passos: [deploy, testes manuais, migrações a aplicar, etc.]
```

## Worked Example

**Input (invocação com PRD):**

```
PRD de Melhoria — Notificações in-app

Contexto: Usuários não sabem quando uma tradução termina de processar.

Funcionalidades:
- Ícone de sino no header com badge de não lidas
- Dropdown com lista das últimas notificações
- Clicar navega para a tradução correspondente

Stack do projeto: Cloudflare Workers (Hono) + React + Vite + Cloudflare D1
```

**Output Fase 1:**

```
## Perguntas antes de implementar — Notificações in-app

Analisei o PRD e o projeto (schema.ts, worker/src/index.ts, frontend/src/components/Header.tsx,
worker/src/routes/translations.ts). Encontrei 4 pontos antes de implementar:

### Regras de Negócio
1. Notificações persistem no banco ou são só em memória por sessão? O PRD não menciona
   uma tabela `notifications` — devo criar uma migration no D1?
2. Há limite de notificações armazenadas (ex: últimas 20)? E ao clicar, a notificação
   some da lista ou fica marcada como lida?

### UX / Usabilidade
3. Em mobile (app é mobile-first), o dropdown deve virar um drawer de tela cheia ou
   um modal? O Header.tsx atual tem espaço limitado em telas pequenas.

### Técnicas
4. Para atualizar o badge sem recarregar a página, prefere polling (fetch a cada Xs)
   ou é aceitável atualizar só ao carregar a página? O Cloudflare free plan não suporta
   WebSockets nativamente.

Assim que você responder, implemento em sequência.
```

**Input (respostas do usuário):**

```
1. Sim, criar tabela. 2. Últimas 30, marcar como lida ao clicar.
3. Drawer mobile. 4. Polling a cada 30s.
```

**Output Fase 2:**

```
Implementando com base nas suas respostas:

**[1/5] Migration: tabela notifications**
[edição em worker/migrations/0004_notifications.sql]

**[2/5] Backend: GET /api/notifications + PATCH /api/notifications/:id**
[edição em worker/src/routes/notifications.ts]

**[3/5] Worker: registrar rotas de notificações**
[edição em worker/src/index.ts]

**[4/5] Frontend: componente NotificationBell.tsx (polling 30s + drawer mobile)**
[edição em frontend/src/components/NotificationBell.tsx]

**[5/5] Frontend: integrar sino no Header.tsx**
[edição em frontend/src/components/Header.tsx]

---
Implementação concluída. 5 arquivos editados.
Próximos passos: aplicar migration com `wrangler d1 migrations apply mandarin-db --remote`,
depois `wrangler deploy` e rebuild do frontend.
```

## Out of Scope

Esta skill NÃO lida com:
- Criar projetos do zero → use /claude-system-builder
- Rotear ou classificar PRD (Lovable vs software) → use /prd-router
- Discovery de produto sem PRD formado → use /product-discovery
- Debug de erros isolados sem PRD → tratar diretamente na conversa
- Code review sem intenção de implementar → tratar diretamente na conversa

## Cross-Skill Routing

- PRD ainda não existe e usuário quer estruturar o problema → recomendar /product-discovery
- Após implementação, se foram criadas novas regras de negócio ou decisões técnicas relevantes → recomendar /build-decisions para documentar
- Se durante a análise a "melhoria" for na verdade um projeto novo → parar e recomendar /claude-system-builder

## Common Shortcuts — Do Not Take These

| O que Claude pode pensar | Por que está errado |
|--------------------------|---------------------|
| "O PRD é claro — posso pular as perguntas e implementar direto" | Sempre existem ambiguidades entre PRD e código atual. Edge cases, comportamento de estado, tratamento de erros — o PRD raramente cobre tudo. Investigar é o valor central desta skill. |
| "Vou apresentar as perguntas e já começar a implementar em paralelo" | Implementar antes das respostas gera código que pode precisar ser refeito. A Fase 1 existe para eliminar retrabalho, não para ser decorativa. |
| "Tenho contexto suficiente da conversa — não preciso ler os arquivos do projeto" | O estado atual do código pode estar desalinhado com o PRD. Sem ler os arquivos, risks técnicos e breaking changes ficam invisíveis. |
| "O usuário disse 'pode implementar como quiser' — isso autoriza implementar tudo" | Liberdade geral em uma questão específica não elimina a necessidade de esclarecer outros pontos. Registrar decisão assumida + continuar com o que foi liberado. |
| "Vou adicionar melhorias oportunistas que percebi no código enquanto implemento" | Escopo fechado. Qualquer melhoria não solicitada deve ser mencionada DEPOIS como sugestão futura — nunca implementada sem aprovação explícita. |
| "Não há dúvidas técnicas óbvias — vou pular essa categoria de perguntas" | "Não há dúvidas óbvias" é diferente de "investigei e não encontrei ambiguidades". Sempre verificar as três categorias antes de concluir que alguma está limpa. |

## Before Marking Complete

- [ ] PRD localizado na conversa ou arquivo — ou decline determinístico exibido se ausente
- [ ] Step 0 executado: arquivos do projeto lidos (listar quais na resposta)
- [ ] Step 1 executado: ambiguidades mapeadas em regras de negócio, UX e técnicas
- [ ] Step 2 executado: perguntas apresentadas e AGUARDADAS (Fase 1 encerrada antes de implementar)
- [ ] Fase 2 iniciada SOMENTE após respostas do usuário recebidas
- [ ] Implementação usa convenções do projeto existente (linguagem, estilo, imports)
- [ ] Nenhuma melhoria não solicitada implementada
- [ ] Cada arquivo editado referenciado explicitamente no output com propósito

## After Completing: Log Learning

Adicionar ao final de `references/learnings.md` (criar arquivo se não existir):

```
Data: [hoje]
Projeto: [nome ou URL]
Melhoria: [nome do PRD]
Dúvidas levantadas: [N total — N negócio / N UX / N técnicas]
Dúvida mais crítica: [qual pergunta evitou mais retrabalho]
O que funcionou: [aspecto do fluxo que produziu boa implementação]
O que não funcionou: [onde houve ambiguidade residual ou revisão]
```
