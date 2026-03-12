#!/bin/bash
# Script de release para PyBlaze
# Cria tag, build e GitHub release
#
# Uso: ./scripts/release.sh 1.0.0

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funções
print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_error() {
    echo -e "${RED}✗ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ ${1}${NC}"
}

# Verificar argumentos
if [ -z "$1" ]; then
    print_error "Versão não especificada!"
    echo "Uso: $0 <versão>"
    echo "Exemplo: $0 1.0.0"
    exit 1
fi

VERSION=$1
TAG="v${VERSION}"

# Banner
echo "=========================================="
echo "  PyBlaze - Release ${VERSION}"
echo "=========================================="
echo ""

# Verificar se estamos no branch correto
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    print_warning "Você está no branch '${CURRENT_BRANCH}'"
    read -p "Continuar mesmo assim? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Release cancelado"
        exit 1
    fi
fi

# Verificar se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    print_error "Há mudanças não commitadas!"
    print_info "Commit ou descarte as mudanças antes de fazer release"
    exit 1
fi

# Verificar se a tag já existe
if git rev-parse "$TAG" >/dev/null 2>&1; then
    print_error "Tag ${TAG} já existe!"
    exit 1
fi

# Executar testes
print_info "Executando testes..."
if make test > /dev/null 2>&1; then
    print_success "Todos os testes passaram"
else
    print_error "Testes falharam!"
    exit 1
fi

# Verificar qualidade do código
print_info "Verificando qualidade do código..."
if make check > /dev/null 2>&1; then
    print_success "Verificações de qualidade passaram"
else
    print_error "Verificações de qualidade falharam!"
    exit 1
fi

# Criar executável
print_info "Criando executável..."
if python scripts/build.py; then
    print_success "Executável criado"
else
    print_error "Falha ao criar executável!"
    exit 1
fi

# Criar tag Git
print_info "Criando tag ${TAG}..."
git tag -a "$TAG" -m "Release ${VERSION}"
print_success "Tag criada"

# Push da tag
print_info "Enviando tag para o repositório remoto..."
if git push origin "$TAG"; then
    print_success "Tag enviada"
else
    print_error "Falha ao enviar tag!"
    print_info "Removendo tag local..."
    git tag -d "$TAG"
    exit 1
fi

# Verificar se gh CLI está instalado
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI (gh) não encontrado"
    print_info "Instale com: https://cli.github.com/"
    print_info "Tag criada, mas release do GitHub deve ser feito manualmente"
    exit 0
fi

# Criar release no GitHub
print_info "Criando release no GitHub..."

# Verificar se há executável para anexar
EXE_PATH="dist/PyBlaze.exe"
if [ ! -f "$EXE_PATH" ]; then
    EXE_PATH="dist/PyBlaze"
fi

if [ -f "$EXE_PATH" ]; then
    gh release create "$TAG" \
        "$EXE_PATH" \
        --title "PyBlaze ${VERSION}" \
        --notes "Release ${VERSION}

## 🎮 Novidades

[Descreva as mudanças aqui]

## 📥 Download

- **Windows/Linux/Mac**: Baixe o executável anexado
- **Python**: \`pip install pyblaze\` ou clone o repositório

## 📝 Changelog completo

Ver [CHANGELOG.md](CHANGELOG.md)
"
    print_success "Release criado com executável anexado"
else
    gh release create "$TAG" \
        --title "PyBlaze ${VERSION}" \
        --notes "Release ${VERSION}"
    print_warning "Release criado sem executável (arquivo não encontrado)"
fi

# Sucesso!
echo ""
echo "=========================================="
print_success "Release ${VERSION} concluído!"
echo "=========================================="
echo ""
print_info "Próximos passos:"
echo "  1. Edite as release notes no GitHub"
echo "  2. Atualize o CHANGELOG.md"
echo "  3. Anuncie o release!"
