# Iter 1 — changes applied

## Changes made to SKILL.md

### 1. Critical section: added Miro rule
Added: "Output final sempre vai para o Miro. Na Fase D, crie a CSD como tabela e a Árvore como diagrama no Miro. Se Miro MCP não disponível, fallback para texto."

### 2. Step 0: added Miro verification row
Added row: "Contexto Miro atual | mcp__claude_ai_Miro__context_get | Board ativo"
Added instruction: "Verificação Miro (somente na Fase D): use ToolSearch com select:mcp__claude_ai_Miro__context_get,board_create,table_create,diagram_create"

### 3. Fase A: added deterministic opening template
Added "Quando invocado sem contexto, use esta abertura determinística: [template com preview das 4 fases + Miro mention + Phase A questions]"
Added "Quando contexto parcial for fornecido: abra com 'Aqui está o que já entendi do contexto:' antes de perguntar"

### 4. Fase D: completely rewritten for Miro integration
Old: single text output block
New: 7 steps (D1 ToolSearch, D2 board check/create, D3 table_create for CSD, D4 diagram_create for Tree, D5 doc_create for próximos passos, D6 confirm with user, D7 text fallback)

### 5. Anti-rationalization table: 2 new rows
- "O Miro pode falhar — vou só entregar o texto" → always try Miro first
- "Vou criar um único widget de texto no Miro" → CSD = table, Tree = diagram (separate tools)

### 6. Exit checklist: updated Fase D item
Old: "Output final entregue no formato completo da Fase D"
New: "Fase D executada: tabela CSD + diagrama Árvore + doc próximos passos criados no Miro (ou fallback em texto se Miro indisponível)"
