# Git Conventions — Commit Semântico, Branches e Pull Requests

> **Público-alvo:** Este documento é destinado a agentes de IA e desenvolvedores que precisam seguir um padrão rigoroso de versionamento em projetos colaborativos. Siga estas regras **sempre**, sem exceções, salvo indicação explícita do mantenedor do projeto.

---

## 1. Commits Semânticos (Conventional Commits)

### Formato obrigatório

```
[<tipo>]: <Descrição curta no imperativo>

[corpo opcional — explica o "por quê", não o "o quê"]

[rodapé opcional — BREAKING CHANGE, closes #issue]
```

**Exemplo:**
```
[feat]: Adiciona autenticação via OAuth2

Implementa login social com Google e Facebook usando passport.js.
Adiciona middleware de autenticação para rotas protegidas.

Closes #123
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

- A descrição deve começar com **letra maiúscula** e estar no **imperativo** (ex: "Adiciona", não "adicionado" ou "adicionando").
- Máximo de **72 caracteres** na primeira linha.
- **Não** terminar com ponto final.
- Usar colchetes para o tipo: `[feat]: Adiciona login com Google`.
- Não usar escopo (se precisar especificar contexto, use o corpo do commit).

### Exemplos corretos ✅

```
[feat]: Adiciona autenticação via OAuth2
[fix]: Corrige cálculo de frete para CEPs do Norte
[docs]: Atualiza instruções de instalação
[chore]: Atualiza versão do pandas para 2.2.0
[refactor]: Extrai lógica de feature engineering para módulo separado
[test]: Adiciona testes unitários para o modelo NBO
[perf]: Otimiza consulta BigQuery reduzindo full scan
[ci]: Adiciona etapa de validação de schema no pipeline
[hotfix]: Corrige crash ao receber payload nulo no endpoint /predict
```

### Exemplos errados ❌

```
fix: correção feita           # sem colchetes, vago
update stuff                  # sem tipo, vago
[feat]: Adiciona Login.       # com ponto final (não permitido)
[feat] adiciona login         # falta dois-pontos, minúscula
feat: Adiciona login          # sem colchetes
commit de teste               # sem tipo semântico
wip                           # nunca commitar WIP na branch principal
[feat]:                       # falta a descrição
```

### Breaking Changes

Quando a mudança quebra compatibilidade, adicionar `!` após o tipo e rodapé `BREAKING CHANGE`:

```
[feat]!: Altera contrato do endpoint /recommendations

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

O título deve seguir o mesmo padrão do commit:

```
[<tipo>]: <Descrição resumida>
```

**Exemplos:**
```
[feat]: Adiciona modelo de reranking por CTR
[fix]: Corrige falha no carregamento de features do BigQuery
[chore]: Atualiza dependências de ML para versões estáveis
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
git commit -m "[feat]: Descrição da mudança"

# 4. Manter branch atualizada durante o desenvolvimento
git pull --rebase origin main

# 5. Push da branch
git push -u origin feat/nome-da-feature

# 6. Abrir PR via CLI ou interface web
gh pr create \
  --title "[feat]: Descrição da feature" \
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

## 6. Automação com GitHub CLI para LLMs

Esta seção fornece comandos prontos para agentes de IA automatizarem operações na organização **IA-para-DEVs-SD**.

### Configuração Inicial

```bash
# Verificar autenticação
gh auth status

# Login (se necessário)
gh auth login

# Configurar variáveis de ambiente para a org
export GH_ORG="IA-para-DEVs-SD"
export GH_REPO="grupo-X-nome-do-projeto"  # Substituir X pelo número do grupo
export PROJECT_NUMBER=28                   # Substituir pelo número do project
```

### Estrutura da Organização

A organização **IA-para-DEVs-SD** possui múltiplos times/grupos, cada um com seus próprios repositórios e projects:

```
IA-para-DEVs-SD/
├── grupo-1-dashboard-produtividade-dev
├── grupo-2-semantic-log-explorer
├── grupo-3-plataforma-de-avaliacao-inteligente
├── grupo-4-Conecta-Talentos
├── grupo-5-kirosonar
├── grupo-6-mentoria
└── ... (outros grupos)

Projects:
├── Project #24: Grupo 6 - MentorIA
├── Project #28: Grupo 5 - Kirosonar
└── ... (outros projects)
```

### Trabalhando com a Organização

#### Listar repositórios da org

```bash
# Listar todos os repos
gh repo list $GH_ORG --limit 50

# Com detalhes em JSON
gh repo list $GH_ORG --json name,description,url,defaultBranchRef

# Filtrar por grupo específico
gh repo list $GH_ORG --limit 100 | grep "grupo-1"
gh repo list $GH_ORG --limit 100 | grep "grupo-2"
gh repo list $GH_ORG --limit 100 | grep "grupo-5"

# Buscar repo de um grupo com JSON
gh repo list $GH_ORG --json name,url | jq '.[] | select(.name | contains("grupo-5"))'
```

#### Criar novo repositório na org

```bash
# Criar repo público para qualquer grupo
gh repo create $GH_ORG/$GH_REPO \
  --public \
  --description "Descrição do projeto" \
  --clone

# Exemplos para diferentes grupos
gh repo create $GH_ORG/grupo-7-nome-projeto --public --description "Projeto do Grupo 7"
gh repo create $GH_ORG/grupo-8-nome-projeto --public --description "Projeto do Grupo 8"

# Com README e .gitignore
gh repo create $GH_ORG/$GH_REPO \
  --public \
  --description "Descrição" \
  --gitignore Python \
  --license MIT \
  --add-readme
```

#### Clonar repositório da org

```bash
# Clone usando variável
gh repo clone $GH_ORG/$GH_REPO

# Clone e entra no diretório
gh repo clone $GH_ORG/$GH_REPO && cd $GH_REPO

# Exemplos para diferentes grupos
gh repo clone IA-para-DEVs-SD/grupo-1-dashboard-produtividade-dev
gh repo clone IA-para-DEVs-SD/grupo-2-semantic-log-explorer
gh repo clone IA-para-DEVs-SD/grupo-3-plataforma-de-avaliacao-inteligente
gh repo clone IA-para-DEVs-SD/grupo-4-Conecta-Talentos
gh repo clone IA-para-DEVs-SD/grupo-5-kirosonar
gh repo clone IA-para-DEVs-SD/grupo-6-mentoria
```

### Trabalhando com Projects (Boards)

#### Listar Projects da org

```bash
# Listar todos os projects
gh project list --owner $GH_ORG

# Em formato JSON
gh project list --owner $GH_ORG --format json

# Filtrar project de um grupo específico
gh project list --owner $GH_ORG | grep "Grupo 1"
gh project list --owner $GH_ORG | grep "Grupo 2"
gh project list --owner $GH_ORG | grep "Grupo 5"

# Ver detalhes de um project específico por número
gh api graphql -f query='
{
  organization(login: "IA-para-DEVs-SD") {
    projectV2(number: 28) {
      title
      shortDescription
      url
      number
    }
  }
}'
```

#### Criar novo Project

```bash
# Criar project genérico na org
gh project create \
  --owner $GH_ORG \
  --title "Nome do Projeto" \
  --format "board"

# Exemplos para diferentes grupos
gh project create --owner $GH_ORG --title "Grupo 7 - Nome do Projeto" --format "board"
gh project create --owner $GH_ORG --title "Grupo 8 - Nome do Projeto" --format "board"
gh project create --owner $GH_ORG --title "Grupo 9 - Nome do Projeto" --format "board"
```

#### Criar cards (draft issues) diretamente no Project

Você pode criar cards no board **sem precisar criar issue primeiro**. Isso é útil para planejamento rápido:

```bash
# Criar draft card usando GraphQL API
gh api graphql -f query='
mutation {
  addProjectV2DraftIssue(input: {
    projectId: "PROJECT_ID"
    title: "[feat]: Título do card"
    body: "Descrição do card"
  }) {
    projectItem {
      id
    }
  }
}'

# Exemplo prático: primeiro pegue o PROJECT_ID
PROJECT_ID=$(gh api graphql -f query='
{
  organization(login: "IA-para-DEVs-SD") {
    projectV2(number: 28) {
      id
    }
  }
}' --jq '.data.organization.projectV2.id')

# Depois crie o card
gh api graphql -f query="
mutation {
  addProjectV2DraftIssue(input: {
    projectId: \"$PROJECT_ID\"
    title: \"[feat]: Implementar dashboard\"
    body: \"Criar dashboard com métricas principais\"
  }) {
    projectItem {
      id
    }
  }
}"

# Criar múltiplos cards de uma vez
for TITLE in "Setup inicial" "Criar API" "Implementar frontend" "Testes"; do
  gh api graphql -f query="
  mutation {
    addProjectV2DraftIssue(input: {
      projectId: \"$PROJECT_ID\"
      title: \"[feat]: $TITLE\"
    }) {
      projectItem {
        id
      }
    }
  }"
done
```

#### Adicionar issue/PR existente ao Project

```bash
# Adicionar issue ao project usando variáveis
gh project item-add $PROJECT_NUMBER \
  --owner $GH_ORG \
  --url https://github.com/$GH_ORG/$GH_REPO/issues/1

# Adicionar PR ao project
gh project item-add $PROJECT_NUMBER \
  --owner $GH_ORG \
  --url https://github.com/$GH_ORG/$GH_REPO/pull/5

# Exemplos para diferentes grupos
gh project item-add 24 --owner IA-para-DEVs-SD --url https://github.com/IA-para-DEVs-SD/grupo-6-mentoria/issues/1
gh project item-add 28 --owner IA-para-DEVs-SD --url https://github.com/IA-para-DEVs-SD/grupo-5-kirosonar/pull/5
```

#### Listar items de um Project

```bash
# Ver todos os items de um project usando variável
gh project item-list $PROJECT_NUMBER --owner $GH_ORG

# Em formato JSON
gh project item-list $PROJECT_NUMBER \
  --owner $GH_ORG \
  --format json \
  --limit 100

# Exemplos para diferentes groups
gh project item-list 24 --owner IA-para-DEVs-SD  # Grupo 6
gh project item-list 28 --owner IA-para-DEVs-SD  # Grupo 5
```

### Trabalhando com Issues

#### Criar issue em repo da org

```bash
# Criar issue usando variáveis
gh issue create \
  --repo $GH_ORG/$GH_REPO \
  --title "[feat]: Nova funcionalidade" \
  --body "Descrição detalhada da issue"

# Criar com labels e assignee
gh issue create \
  --repo $GH_ORG/$GH_REPO \
  --title "[bug]: Erro no login" \
  --body "Descrição do bug" \
  --label "bug,priority-high" \
  --assignee @me

# Exemplos para diferentes grupos
gh issue create --repo IA-para-DEVs-SD/grupo-1-dashboard-produtividade-dev --title "[feat]: Nova feature"
gh issue create --repo IA-para-DEVs-SD/grupo-2-semantic-log-explorer --title "[fix]: Corrige bug"
gh issue create --repo IA-para-DEVs-SD/grupo-5-kirosonar --title "[docs]: Atualiza docs"
```

#### Listar issues

```bash
# Listar issues abertas usando variável
gh issue list --repo $GH_ORG/$GH_REPO

# Com filtros
gh issue list \
  --repo $GH_ORG/$GH_REPO \
  --state all \
  --label "bug" \
  --assignee @me

# Listar issues de diferentes grupos
gh issue list --repo IA-para-DEVs-SD/grupo-1-dashboard-produtividade-dev
gh issue list --repo IA-para-DEVs-SD/grupo-5-kirosonar
gh issue list --repo IA-para-DEVs-SD/grupo-6-mentoria
```

### Trabalhando com Pull Requests

#### Criar PR no repo da org

```bash
# PR básico usando variáveis
gh pr create \
  --repo $GH_ORG/$GH_REPO \
  --title "[feat]: Adiciona autenticação" \
  --body "Implementa sistema de login" \
  --base main \
  --head feat/auth

# PR com reviewers e labels
gh pr create \
  --repo $GH_ORG/$GH_REPO \
  --title "[feat]: Adiciona dashboard" \
  --body "$(cat .github/pull_request_template.md)" \
  --base main \
  --reviewer username1,username2 \
  --label "enhancement,ready-for-review"

# Exemplos para diferentes grupos
gh pr create --repo IA-para-DEVs-SD/grupo-1-dashboard-produtividade-dev --title "[feat]: Nova feature" --base main
gh pr create --repo IA-para-DEVs-SD/grupo-5-kirosonar --title "[fix]: Corrige bug" --base main
```

#### Listar PRs

```bash
# PRs abertas usando variável
gh pr list --repo $GH_ORG/$GH_REPO

# Todas as PRs
gh pr list --repo $GH_ORG/$GH_REPO --state all

# Listar PRs de diferentes grupos
gh pr list --repo IA-para-DEVs-SD/grupo-1-dashboard-produtividade-dev
gh pr list --repo IA-para-DEVs-SD/grupo-5-kirosonar
gh pr list --repo IA-para-DEVs-SD/grupo-6-mentoria
```

#### Merge de PR

```bash
# Merge com squash (recomendado) usando variável
gh pr merge 123 \
  --repo $GH_ORG/$GH_REPO \
  --squash \
  --delete-branch

# Auto-merge quando CI passar
gh pr merge 123 \
  --repo $GH_ORG/$GH_REPO \
  --squash \
  --auto
```

### Script Helper: Criar Cards no Board

Script prático para LLMs criarem cards rapidamente:

```bash
#!/bin/bash
# Helper: Criar cards no project board
# Uso: ./create-card.sh "Título do card" "Descrição (opcional)"

# ==================== CONFIGURAÇÃO ====================
ORG="IA-para-DEVs-SD"
PROJECT_NUMBER=28  # Mudar para o número do seu project
# =====================================================

# Pegar PROJECT_ID
PROJECT_ID=$(gh api graphql -f query="
{
  organization(login: \"$ORG\") {
    projectV2(number: $PROJECT_NUMBER) {
      id
    }
  }
}" --jq '.data.organization.projectV2.id')

# Validar
if [ -z "$PROJECT_ID" ]; then
  echo "❌ Erro: Project #$PROJECT_NUMBER não encontrado"
  exit 1
fi

# Parâmetros
TITLE="$1"
BODY="${2:-}"

if [ -z "$TITLE" ]; then
  echo "❌ Uso: $0 \"Título do card\" \"Descrição (opcional)\""
  exit 1
fi

# Criar card
echo "📝 Criando card no Project #$PROJECT_NUMBER..."

RESULT=$(gh api graphql -f query="
mutation {
  addProjectV2DraftIssue(input: {
    projectId: \"$PROJECT_ID\"
    title: \"$TITLE\"
    body: \"$BODY\"
  }) {
    projectItem {
      id
    }
  }
}" --jq '.data.addProjectV2DraftIssue.projectItem.id')

if [ -n "$RESULT" ]; then
  echo "✅ Card criado com sucesso!"
  echo "   Título: $TITLE"
  echo "   ID: $RESULT"
else
  echo "❌ Erro ao criar card"
  exit 1
fi
```

**Exemplos de uso do script:**

```bash
# Criar card simples
./create-card.sh "[feat]: Implementar login"

# Criar card com descrição
./create-card.sh "[feat]: Dashboard" "Criar dashboard com métricas de uso"

# Criar múltiplos cards de backlog
./create-card.sh "[feat]: Setup inicial do projeto"
./create-card.sh "[feat]: Configurar banco de dados"
./create-card.sh "[feat]: Criar API REST"
./create-card.sh "[feat]: Implementar autenticação"
./create-card.sh "[test]: Adicionar testes unitários"
./create-card.sh "[docs]: Documentar API"
```

### Workflow Completo para LLM

Este script pode ser adaptado para **qualquer grupo** da organização:

```bash
#!/bin/bash
# Script de automação completo para LLM criar feature em repo da org
# CONFIGURE AS VARIÁVEIS ABAIXO PARA O SEU GRUPO

# ==================== CONFIGURAÇÃO ====================
ORG="IA-para-DEVs-SD"
REPO="grupo-X-nome-do-projeto"      # Substituir pelo repo do seu grupo
FEATURE_NAME="nome-da-feature"      # Nome da feature a implementar
PROJECT_NUMBER=XX                    # Número do project do seu grupo
# =====================================================

# 1. Clonar repo (se ainda não tiver)
gh repo clone $ORG/$REPO
cd $REPO

# 2. Atualizar main
git checkout main
git pull origin main

# 3. Criar branch
git checkout -b feat/$FEATURE_NAME

# 4. [DESENVOLVER CÓDIGO AQUI]
# ...

# 5. Commit
git add .
git commit -m "[feat]: Adiciona $FEATURE_NAME"

# 6. Push
git push -u origin feat/$FEATURE_NAME

# 7. Criar PR
PR_URL=$(gh pr create \
  --title "[feat]: Adiciona $FEATURE_NAME" \
  --body "Implementação completa de $FEATURE_NAME" \
  --base main \
  --fill | grep -o 'https://.*')

# 8. Adicionar PR ao Project
gh project item-add $PROJECT_NUMBER \
  --owner $ORG \
  --url $PR_URL

echo "✅ PR criada e adicionada ao project: $PR_URL"
```

**Exemplos configurados para diferentes grupos:**

```bash
# Grupo 1
ORG="IA-para-DEVs-SD"
REPO="grupo-1-dashboard-produtividade-dev"
PROJECT_NUMBER=XX  # Buscar com: gh project list --owner IA-para-DEVs-SD

# Grupo 2
ORG="IA-para-DEVs-SD"
REPO="grupo-2-semantic-log-explorer"
PROJECT_NUMBER=XX

# Grupo 5
ORG="IA-para-DEVs-SD"
REPO="grupo-5-kirosonar"
PROJECT_NUMBER=28

# Grupo 6
ORG="IA-para-DEVs-SD"
REPO="grupo-6-mentoria"
PROJECT_NUMBER=24
```

### Comandos Úteis para Exploração

```bash
# Ver detalhes de um repo usando variável
gh repo view $GH_ORG/$GH_REPO

# Ver issues e PRs de um repo no browser
gh repo view $GH_ORG/$GH_REPO --web

# Ver informações da org
gh api orgs/$GH_ORG | jq

# Buscar repos de um grupo específico
gh repo list $GH_ORG --limit 100 | grep -i "grupo-1"
gh repo list $GH_ORG --limit 100 | grep -i "grupo-5"
gh repo list $GH_ORG --limit 100 | grep -i "grupo-6"

# Ver todos os repos da org
gh repo list $GH_ORG --limit 100

# Ver members da org (se tiver permissão)
gh api orgs/$GH_ORG/members

# Ver teams da org
gh api orgs/$GH_ORG/teams

# Buscar repo por palavra-chave
gh repo list $GH_ORG --json name,description | jq '.[] | select(.description | contains("mentoria"))'
gh repo list $GH_ORG --json name,description | jq '.[] | select(.description | contains("dashboard"))'
```

### Template de Issue para LLM

```bash
# Criar issue formatada
gh issue create \
  --repo IA-para-DEVs-SD/$REPO \
  --title "[feat]: Título da feature" \
  --body "$(cat <<'EOF'
## Descrição
[Descreva a feature]

## Motivação
[Por que essa feature é necessária?]

## Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

## Tarefas
- [ ] Tarefa 1
- [ ] Tarefa 2
- [ ] Tarefa 3

## Observações
[Informações adicionais]
EOF
)"
```

### Template de PR para LLM

```bash
# Criar PR formatada
gh pr create \
  --repo IA-para-DEVs-SD/$REPO \
  --title "[feat]: Título da feature" \
  --body "$(cat <<'EOF'
## O que foi feito
- Implementação de X
- Adição de Y
- Correção de Z

## Motivação
Essa mudança resolve o problema de [descrever].

## Como testar
1. Clone a branch
2. Execute `npm install`
3. Execute `npm test`
4. Verifique que todos os testes passam

## Screenshots (se aplicável)
[Adicionar screenshots]

## Checklist
- [x] Código segue os padrões do projeto
- [x] Testes foram adicionados/atualizados
- [x] Documentação foi atualizada
- [x] Sem segredos ou credenciais no código
- [x] Branch está atualizada com main

## Issues relacionadas
Closes #123
EOF
)" \
  --base main
```

### Dicas para LLMs

1. **Sempre configurar variáveis no início:**
   ```bash
   export GH_ORG="IA-para-DEVs-SD"
   export GH_REPO="grupo-X-nome-projeto"  # Substituir X
   export PROJECT_NUMBER=XX                # Buscar número correto
   ```

2. **Descobrir qual repo trabalhar:**
   ```bash
   # Listar todos
   gh repo list $GH_ORG --limit 50

   # Filtrar por grupo
   gh repo list $GH_ORG | grep "grupo-5"
   ```

3. **Descobrir número do project:**
   ```bash
   # Listar todos os projects
   gh project list --owner $GH_ORG

   # Buscar project de um grupo específico
   gh project list --owner $GH_ORG | grep "Grupo 5"
   ```

4. **Verificar antes de operar:**
   ```bash
   # Verificar se repo existe
   gh repo view $GH_ORG/$GH_REPO

   # Verificar autenticação
   gh auth status
   ```

5. **Sempre usar commits semânticos:**
   ```bash
   [feat]: Descrição
   [fix]: Descrição
   [docs]: Descrição
   ```

6. **Adicionar items aos projects automaticamente:**
   ```bash
   # Após criar issue/PR, adicionar ao project
   gh project item-add $PROJECT_NUMBER --owner $GH_ORG --url $ITEM_URL
   ```

7. **Usar JSON para parsing de dados:**
   ```bash
   # Buscar repo específico
   gh repo list $GH_ORG --json name,url | jq '.[] | select(.name | contains("grupo-5"))'

   # Buscar project específico
   gh project list --owner $GH_ORG --format json | jq '.projects[] | select(.title | contains("Grupo 5"))'
   ```

8. **Trabalhar com múltiplos grupos:**
   ```bash
   # Loop para operar em múltiplos grupos
   for GRUPO in grupo-1 grupo-2 grupo-5; do
     gh repo clone $GH_ORG/$GRUPO-*
   done
   ```

9. **Criar cards no board para planejamento:**
   ```bash
   # Pegar ID do project
   PROJECT_ID=$(gh api graphql -f query='
   {
     organization(login: "IA-para-DEVs-SD") {
       projectV2(number: 28) {
         id
       }
     }
   }' --jq '.data.organization.projectV2.id')

   # Criar card
   gh api graphql -f query="
   mutation {
     addProjectV2DraftIssue(input: {
       projectId: \"$PROJECT_ID\"
       title: \"[feat]: Nova feature\"
       body: \"Descrição da feature\"
     }) {
       projectItem {
         id
       }
     }
   }"
   ```

10. **Criar backlog completo no board:**
    ```bash
    # Definir array de tarefas
    TASKS=(
      "[feat]: Setup do projeto"
      "[feat]: Implementar autenticação"
      "[feat]: Criar dashboard"
      "[test]: Adicionar testes"
      "[docs]: Documentar API"
    )

    # Criar todos os cards
    for TASK in "${TASKS[@]}"; do
      gh api graphql -f query="
      mutation {
        addProjectV2DraftIssue(input: {
          projectId: \"$PROJECT_ID\"
          title: \"$TASK\"
        }) {
          projectItem { id }
        }
      }"
      echo "✅ Card criado: $TASK"
    done
    ```

---

## 7. Referência Rápida

```
COMMIT:   [<tipo>]: <Descrição imperativa, maiúscula, sem ponto>
BRANCH:   <tipo>/<descricao-em-kebab-case>
PR TITLE: [<tipo>]: <Descrição resumida>

Tipos válidos: feat | fix | docs | style | refactor | test | chore | perf | ci | hotfix | revert

Exemplos de commits válidos:
  - [feat]: Adiciona login com Google
  - [fix]: Corrige timeout em requisições
  - [docs]: Atualiza README com novas instruções
  - [chore]: Atualiza dependências do projeto

NUNCA:
  - Commitar direto na main
  - Usar "wip", "update", "fix stuff" como mensagem de commit
  - Esquecer os colchetes: feat: descrição
  - Começar descrição com letra minúscula
  - Terminar descrição com ponto final
  - Abrir PR sem descrição
  - Fazer merge com CI vermelho
  - Deixar branches mortas após o merge
```