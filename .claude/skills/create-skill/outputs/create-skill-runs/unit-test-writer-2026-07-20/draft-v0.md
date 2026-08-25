---
name: unit-test-writer
description: Gera testes unitários para o código que está sendo desenvolvido no momento, detectando automaticamente a linguagem, o framework de testes e as convenções (pasta, naming, estilo de assertion) já usadas no projeto, cobrindo caminho de sucesso, edge cases e casos de erro, e executando os testes de verdade para confirmar que passam. Use quando o usuário disser 'cria testes unitários para isso', 'escreve os testes desse arquivo', 'gera testes para essa função', 'testa esse código', 'preciso de testes para o que acabei de escrever', 'write unit tests for this', ou pedir cobertura de testes para uma função/classe/módulo específico. Do NOT use para testes de integração ou end-to-end de fluxo completo → use /verify. Do NOT use para revisão geral de bugs/qualidade → use /code-review. Do NOT use para revisão de segurança → use /security-review. Do NOT use para refatorar o código-fonte → use /simplify.
---

# unit-test-writer

Gera testes unitários para código recém-escrito ou em desenvolvimento, sempre ancorado nas convenções reais do projeto — nunca em um framework ou estilo genérico "de treino". Detecta linguagem e framework de testes existentes, projeta casos de sucesso, edge case e erro, escreve os testes no formato e local corretos, e executa os testes de verdade antes de reportar qualquer resultado.

## Critical

- **Nunca declare que os testes passam sem executá-los.** Rodar os testes é uma etapa obrigatória, não opcional. Se não for possível executar (ambiente sem dependências instaladas, sem acesso ao terminal), diga isso explicitamente — nunca simule um resultado.
- **Nunca altere o código de produção para forçar um teste a passar.** Se um teste falha porque o teste está errado, corrija o teste. Se um teste falha porque revelou um bug real no código, PARE, reporte o bug encontrado com a linha exata, e pergunte ao usuário antes de tocar no código-fonte.
- **Nunca invente uma convenção silenciosamente.** Se o projeto não tem testes existentes para copiar o padrão, escolha o framework/estilo mais comum para a linguagem detectada e marque a escolha como `[DEFAULT: <framework/local/naming> — confirmar com o usuário]`.
- **Não teste código que não existe.** Se o usuário não indicou qual arquivo/função testar e não há edição recente na conversa, pergunte qual código deve ser testado em vez de inventar um exemplo genérico.

## Step 0: Detectar Contexto do Projeto

Antes de escrever qualquer teste, investigue o projeto real. Nunca assuma framework ou convenção sem checar.

| Fonte | Onde procurar | O que extrair |
|-------|----------------|----------------|
| Código-alvo | Arquivo(s) citados pelo usuário, ou o(s) arquivo(s) editado/criado mais recentemente nesta conversa | Funções/métodos públicos, parâmetros, tipos de retorno, exceções lançadas, branches condicionais |
| Manifesto de dependências | `package.json`, `requirements.txt` / `pyproject.toml`, `go.mod`, `Cargo.toml`, `composer.json`, `*.csproj`, `Gemfile` (o que existir na raiz do repo) | Linguagem, framework de teste já instalado (jest, vitest, pytest, unittest, go test, JUnit, RSpec, PHPUnit, xUnit, etc.) |
| Testes existentes | Buscar arquivos como `**/*.test.*`, `**/*.spec.*`, `**/test_*.py`, `**/*_test.go`, pastas `tests/`, `__tests__/`, `spec/` | Local exato (pasta espelhada vs. colocada junto), convenção de nome, estilo de assertion (`expect().toBe()`, `assert`, `assertEquals`), padrão de mock/fixture, uso de `describe`/`it` vs. funções soltas |
| Config de teste | `jest.config.*`, `vitest.config.*`, `pytest.ini`, `phpunit.xml`, `.rspec`, scripts em `package.json` | Comando exato para rodar os testes, thresholds de cobertura, aliases de path |
| CI (opcional) | `.github/workflows/*.yml` ou equivalente | Comando de teste usado em CI, para rodar localmente o mesmo comando |

Se nenhum teste existente for encontrado, siga em frente com o Passo 1 mas aplique a regra de `[DEFAULT: ...]` do bloco Critical ao escolher framework/local/naming.

## Passo 1: Identificar o Código-Alvo

Se o usuário nomeou um arquivo, função ou classe, use exatamente esse alvo. Se disse apenas "isso" ou "esse código", identifique o(s) arquivo(s) editado(s)/criado(s) mais recentemente na conversa atual. Se não houver alvo identificável, pare e pergunte qual arquivo/função deve ser testado — não gere um exemplo genérico.

## Passo 2: Projetar os Casos de Teste

Para cada função/método público do alvo, liste os casos antes de escrever qualquer código, cobrindo três categorias:

1. **Caminho de sucesso** — input válido típico, comportamento esperado.
2. **Edge cases** — limites (0, vazio, string vazia, lista vazia, valor máximo/mínimo, null/undefined/None, duplicatas, unicode quando relevante).
3. **Casos de erro** — input inválido, tipo errado, dependência externa falhando, exceção esperada.

Se uma das três categorias genuinamente não se aplica (ex: função pura sem forma de erro), declare isso explicitamente em vez de omitir silenciosamente.

## Passo 3: Escrever os Testes

Escreva os testes seguindo exatamente a convenção detectada no Step 0:
- Mesma pasta/local dos testes existentes (ou `[DEFAULT: ...]` se não houver nenhum).
- Mesmo naming de arquivo e de casos de teste.
- Mesmo estilo de assertion e de mock/fixture já usado no projeto.
- Um caso de teste por comportamento — não agrupe múltiplas asserções não relacionadas num único teste.

## Passo 4: Executar os Testes

Rode o comando de teste real do projeto (detectado no Step 0, ou o comando padrão do framework se não houver script customizado). Capture a saída completa.

- Se todos os testes novos passam: reporte o comando usado e o resumo da saída (quantos passaram).
- Se algum teste falha porque o teste está incorreto: corrija o teste e rode de novo.
- Se algum teste falha porque expôs um bug real no código-alvo: NÃO corrija o código-fonte. Reporte o bug com arquivo:linha e o motivo da falha, e pergunte ao usuário como prosseguir.

## Output Format

Para cada arquivo de teste gerado, reporte nesta estrutura:

```
## Testes gerados: <caminho do arquivo de teste>

Framework detectado: <framework> [DEFAULT: ... — confirmar com o usuário] (se aplicável)
Convenção seguida: <descrição breve — ex: "mesma pasta __tests__, estilo describe/it, mocks com jest.mock">

### Casos cobertos
- Sucesso: <lista breve>
- Edge cases: <lista breve>
- Erros: <lista breve>

### Código do teste
<bloco de código completo>

### Execução
Comando: `<comando real rodado>`
Resultado: <X passed, Y failed — resumo real da saída, nunca simulado>
```

## Worked Example (com convenção existente)

Entrada do usuário: "cria testes unitários para a função `calculateDiscount` em `src/utils/pricing.js`"

Step 0 encontra: `package.json` com `"jest": "^29"` e script `"test": "jest"`; testes existentes em `src/utils/__tests__/*.test.js` usando `describe`/`it` e `expect().toBe()`.

Saída:

```
## Testes gerados: src/utils/__tests__/pricing.test.js

Framework detectado: Jest (via package.json)
Convenção seguida: mesma pasta __tests__ ao lado do módulo, describe/it, expect().toBe()

### Casos cobertos
- Sucesso: desconto de 10% sobre preço válido; desconto de 0% retorna preço original
- Edge cases: preço = 0; desconto = 100%; preço com casas decimais longas
- Erros: preço negativo lança erro; desconto > 100 lança erro; desconto negativo lança erro

### Código do teste
describe('calculateDiscount', () => {
  it('aplica desconto percentual corretamente', () => {
    expect(calculateDiscount(100, 10)).toBe(90);
  });
  it('retorna o preço original quando desconto é 0', () => {
    expect(calculateDiscount(100, 0)).toBe(100);
  });
  it('lida com preço igual a zero', () => {
    expect(calculateDiscount(0, 10)).toBe(0);
  });
  it('lança erro para preço negativo', () => {
    expect(() => calculateDiscount(-10, 10)).toThrow();
  });
  it('lança erro para desconto acima de 100%', () => {
    expect(() => calculateDiscount(100, 150)).toThrow();
  });
});

### Execução
Comando: `npx jest src/utils/__tests__/pricing.test.js`
Resultado: 5 passed, 0 failed
```

## Worked Example (sem convenção existente — DEFAULT)

Entrada do usuário: "/unit-test-writer" (sem contexto, projeto Python novo sem nenhum teste ainda)

Saída esperada: Step 0 não encontra testes existentes nem framework declarado em `requirements.txt`/`pyproject.toml`. A skill pergunta qual arquivo/função testar (Passo 1) e, ao gerar, marca a escolha de framework como `[DEFAULT: pytest — framework mais comum para Python puro, confirmar com o usuário]` e propõe local `tests/test_<modulo>.py`, deixando claro que é uma escolha padrão, não uma convenção detectada.

## Out of Scope

Esta skill NÃO cobre:
- Testes de integração ou end-to-end de um fluxo completo → use `/verify`
- Revisão geral de bugs, segurança ou qualidade do diff → use `/code-review`
- Revisão focada em segurança → use `/security-review`
- Refatoração ou simplificação do código-fonte → use `/simplify`
- Subir/rodar a aplicação para checar manualmente no navegador → use `/run`

## Cross-Skill Routing

- Se a execução dos testes revelar um bug real no código-alvo → reporte o bug e sugira `/code-review` para uma revisão mais ampla antes de prosseguir
- Se o usuário pedir para validar a feature completa funcionando de ponta a ponta (não só as unidades) → recomende `/verify`
- Se não houver como rodar os testes localmente (app precisa estar de pé) → recomende `/run` primeiro

## Common Shortcuts — Do Not Take These

| What Claude might think | Why it's wrong |
|---|---|
| "O projeto usa uma linguagem que eu conheço bem, posso pular o Step 0" | Frameworks e convenções variam por projeto mesmo dentro da mesma linguagem (jest vs. vitest vs. mocha). Pular o Step 0 gera testes no formato errado. |
| "Escrevi os testes, parecem corretos, não preciso rodar" | "Parecem corretos" não é o mesmo que passar. A regra Critical exige execução real antes de reportar qualquer resultado. |
| "O teste falhou, mais rápido corrigir o código-fonte do que investigar" | Alterar o código-alvo silenciosamente pode mascarar um bug real ou mudar comportamento sem autorização do usuário. Sempre pare e pergunte. |
| "Não achei testes existentes, vou usar o framework mais popular sem avisar" | Isso é um default não confirmado se passando por convenção do projeto. Sempre marque com `[DEFAULT: ... — confirmar com o usuário]`. |
| "O usuário disse 'testa isso' sem nomear arquivo, vou inventar um exemplo" | Gera testes para código que não existe. Pare e pergunte qual arquivo/função é o alvo. |

## Before Marking Complete

Não considere a tarefa concluída até que todos os itens abaixo sejam verdadeiros:

- [ ] Step 0 foi executado — framework, convenção de pasta/naming e comando de teste foram identificados (ou explicitamente marcados como não encontrados)
- [ ] O código-alvo foi identificado a partir do pedido do usuário ou de edições recentes na conversa — nunca inventado
- [ ] Os casos de teste cobrem sucesso, edge cases e erros (ou a ausência de uma categoria foi declarada explicitamente)
- [ ] O arquivo de teste segue a convenção real do projeto, com qualquer escolha não encontrada marcada como `[DEFAULT: ... — confirmar com o usuário]`
- [ ] Os testes foram executados de verdade e a saída real (comando + resultado) está no report — nunca um resultado presumido
- [ ] Se algum teste revelou um bug no código-alvo, o código-fonte NÃO foi alterado sem antes reportar e perguntar ao usuário

Se algum item acima não estiver marcado, complete-o antes de finalizar.
