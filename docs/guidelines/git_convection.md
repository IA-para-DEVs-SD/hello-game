# Git Conventions — Commit Semântico, Branches e Pull Requests

> **Público-alvo:** Este documento é destinado a agentes de IA e desenvolvedores que precisam seguir um padrão rigoroso de versionamento em projetos colaborativos. Siga estas regras **sempre**, sem exceções, salvo indicação explícita do mantenedor do projeto.

---

## 1. Commits Semânticos (Conventional Commits)

### Formato obrigatório

```
<tipo>(<escopo opcional>): <descrição curta no imperativo>

[corpo opcional — explica o "por quê", não o "o quê"]

[rodapé opcional — BREAKING CHANGE, closes #issue]
```

### Tipos permitidos

| Tipo       | Quando usar                                                              |
|------------|--------------------------------------------------------------------------|
| `feat`     | Nova funcionalidade visível ao usuário                                   |
| `fix`      | Correção de bug                                                          |
| `docs`     | Alteração apenas em documentação                                         |
| `style`    | Formatação, ponto e vírgula, espaços — sem mudança de lógica            |
| `refactor` | Refatoração de código sem nova feature nem fix                           |
| `test`     | Adição ou correção de testes                                             |
| `chore`    | Tarefas de manutenção: deps, build, CI — sem impacto no código de prod  |
| `perf`     | Melhoria de performance                                                  |
| `ci`       | Mudanças em pipelines de CI/CD                                           |
| `hotfix`   | Correção crítica aplicada diretamente em produção                        |
| `revert`   | Reverter um commit anterior                                              |

### Regras de escrita

- A descrição deve estar em **letras minúsculas** e no **imperativo** (ex: "adiciona", não "adicionado" ou "adicionando").
- Máximo de **72 caracteres** na primeira linha.
- **Não** terminar com ponto final.
- Escopo é opcional mas recomendado: `feat(auth): adiciona login com Google`.

### Exemplos corretos ✅

```
feat(auth): adiciona autenticação via OAuth2
fix(cart): corrige cálculo de frete para CEPs do Norte
docs(readme): atualiza instruções de instalação
chore(deps): atualiza versão do pandas para 2.2.0
refactor(pipeline): extrai lógica de feature engineering para módulo separado
test(recommender): adiciona testes unitários para o modelo NBO
perf(query): otimiza consulta BigQuery reduzindo full scan
ci(vertex): adiciona etapa de validação de schema no pipeline
hotfix(api): corrige crash ao receber payload nulo no endpoint /predict
```

### Exemplos errados ❌

```
fix: correção feita           # não diz O QUE foi corrigido
update stuff                  # sem tipo, vago
feat: Adiciona Login.         # inicial maiúscula + ponto final
commit de teste               # sem tipo semântico
wip                           # nunca commitar WIP na branch principal
```

### Breaking Changes

Quando a mudança quebra compatibilidade, adicionar `!` após o tipo e rodapé `BREAKING CHANGE`:

```
feat(api)!: altera contrato do endpoint /recommendations

BREAKING CHANGE: o campo `user_id` foi renomeado para `userId` no request body.
Clientes devem atualizar a integração antes de usar esta versão.
```

---

## 2. Criação de Branches

### Formato obrigatório

```
<tipo>/<descricao-em-kebab-case>
```

### Tipos de branch

| Prefixo      | Finalidade                                             |
|--------------|--------------------------------------------------------|
| `feat/`      | Nova funcionalidade                                    |
| `fix/`       | Correção de bug                                        |
| `hotfix/`    | Correção crítica urgente (a partir da `main`)          |
| `docs/`      | Apenas documentação                                    |
| `refactor/`  | Refatoração sem mudança de comportamento               |
| `test/`      | Testes novos ou ajustes em testes existentes           |
| `chore/`     | Manutenção geral (deps, configs, scripts)              |
| `ci/`        | Mudanças em CI/CD                                      |
| `release/`   | Preparação de versão (bump de versão, changelogs)      |

### Regras de nomenclatura

- Usar apenas **letras minúsculas**, **números** e **hífens** (`-`).
- **Sem** espaços, underscores ou caracteres especiais.
- Descrição deve ser **curta e descritiva** (máx. ~40 chars após o prefixo).
- Branches devem partir de `main` (ou `develop`, se o projeto usar GitFlow).

### Exemplos corretos ✅

```
feat/user-registration
fix/null-pointer-on-checkout
hotfix/api-crash-empty-payload
docs/api-reference-update
refactor/feature-engineering-module
test/nbo-unit-tests
chore/upgrade-python-3-12
ci/add-vertex-schema-validation
release/v2.3.0
```

### Exemplos errados ❌

```
minhaFeature          # sem prefixo, camelCase
fix_login_bug         # underscores não permitidos
FEAT/login            # maiúsculas não permitidas
feature/              # sem descrição
temp                  # sem contexto
branch-do-joao        # nome pessoal sem contexto
```

### Branches protegidas

| Branch      | Regra                                                              |
|-------------|--------------------------------------------------------------------|
| `main`      | **Nunca** recebe push direto. Apenas via PR aprovado.             |
| `develop`   | Pode receber merges de `feat/`, `fix/`, `refactor/` via PR.       |
| `release/*` | Apenas bugfixes e bumps de versão. Merge em `main` e `develop`.   |
| `hotfix/*`  | Parte de `main`. Merge em `main` e `develop` após correção.       |

---

## 3. Pull Requests (PRs)

### Quando abrir um PR

- Sempre que uma branch estiver pronta para revisão, independente do tamanho.
- PRs de trabalho em progresso devem ser abertos como **Draft PR**.
- **Nunca** fazer merge direto na `main` sem PR (exceto hotfix emergencial com aprovação explícita do mantenedor).

### Formato do título do PR

O título deve seguir o mesmo padrão do commit semântico:

```
<tipo>(<escopo>): <descrição resumida>
```

**Exemplos:**
```
feat(recommender): adiciona modelo de reranking por CTR
fix(pipeline): corrige falha no carregamento de features do BigQuery
chore(deps): atualiza dependências de ML para versões estáveis
```

### Template de descrição obrigatório

Todo PR deve conter no corpo:

```markdown
## O que foi feito
<!-- Descreva as mudanças realizadas de forma objetiva -->
- 

## Motivação
<!-- Por que essa mudança é necessária? Qual problema resolve? -->

## Como testar
<!-- Passos para validar as mudanças localmente ou em staging -->
1. 
2. 

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada (se necessário)
- [ ] Sem segredos ou credenciais no código
- [ ] Branch está atualizada com `main`

## Issues relacionadas
<!-- Use "Closes #123" para fechar a issue automaticamente no merge -->
```

### Regras de revisão e merge

| Regra                         | Detalhe                                                                 |
|-------------------------------|-------------------------------------------------------------------------|
| Aprovações mínimas            | Ao menos **1 aprovação** antes do merge (2 para mudanças críticas)      |
| CI deve estar verde           | Nenhum PR pode ser mergeado com checks falhando                         |
| Sem conflitos                 | Resolver conflitos antes de solicitar revisão                           |
| Estratégia de merge           | Prefer **Squash and Merge** para branches de feature                    |
| Merge commit                  | Usar para `release/` e `hotfix/` que precisam manter histórico          |
| Deletar branch após merge     | Sempre deletar a branch após o merge ser concluído                      |

### Tamanho ideal de PR

| Classificação | Linhas alteradas | Ação recomendada                                |
|---------------|------------------|-------------------------------------------------|
| Pequeno       | < 200 linhas     | Pronto para revisão direta                      |
| Médio         | 200–500 linhas   | Adicionar contexto extra na descrição           |
| Grande        | > 500 linhas     | Considerar dividir em PRs menores               |
| Gigante       | > 1000 linhas    | **Obrigatório** dividir antes de abrir          |

---

## 4. Fluxo Completo — Do Código ao Merge

```bash
# 1. Partir sempre de uma main atualizada
git checkout main
git pull origin main

# 2. Criar a branch com nome semântico
git checkout -b feat/nome-da-feature

# 3. Desenvolver e commitar com mensagens semânticas
git add .
git commit -m "feat(escopo): descrição da mudança"

# 4. Manter branch atualizada durante o desenvolvimento
git pull --rebase origin main

# 5. Push da branch
git push -u origin feat/nome-da-feature

# 6. Abrir PR via CLI ou interface web
gh pr create \
  --title "feat(escopo): descrição da feature" \
  --body "$(cat .github/pull_request_template.md)" \
  --base main \
  --assignee @me

# 7. Após aprovação e CI verde: merge (squash) e deletar branch
gh pr merge <numero> --squash --delete-branch
```

---

## 5. Versionamento Semântico (SemVer)

As versões do projeto seguem o padrão `MAJOR.MINOR.PATCH`:

| Versão  | Quando incrementar                                              |
|---------|-----------------------------------------------------------------|
| `MAJOR` | Breaking change (incompatível com versão anterior)             |
| `MINOR` | Nova funcionalidade retrocompatível (`feat`)                    |
| `PATCH` | Correção de bug retrocompatível (`fix`, `hotfix`, `perf`)       |

**Exemplos:**
```
1.0.0 → 1.0.1   # fix: corrige bug de formatação
1.0.1 → 1.1.0   # feat: adiciona exportação em CSV
1.1.0 → 2.0.0   # feat!: remove suporte à API v1 (BREAKING CHANGE)
```

---

## 6. Referência Rápida

```
COMMIT:   <tipo>(<escopo>): <descrição imperativa, minúscula, sem ponto>
BRANCH:   <tipo>/<descricao-em-kebab-case>
PR TITLE: <tipo>(<escopo>): <descrição resumida>

Tipos válidos: feat | fix | docs | style | refactor | test | chore | perf | ci | hotfix | revert

NUNCA:
  - Commitar direto na main
  - Usar "wip", "update", "fix stuff" como mensagem de commit
  - Abrir PR sem descrição
  - Fazer merge com CI vermelho
  - Deixar branches mortas após o merge
```