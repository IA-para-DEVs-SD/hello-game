# Guia de Contribuição - PyBlaze

> Como contribuir para o projeto PyBlaze

---

## 🎯 Bem-vindo!

Obrigado por considerar contribuir com o PyBlaze! Este documento fornece diretrizes para tornar o processo de contribuição claro e eficiente.

---

## 📋 Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como Começar](#como-começar)
3. [Processo de Desenvolvimento](#processo-de-desenvolvimento)
4. [Padrões de Código](#padrões-de-código)
5. [Commits e Pull Requests](#commits-e-pull-requests)
6. [Testes](#testes)
7. [Documentação](#documentação)

---

## 📜 Código de Conduta

Este projeto segue princípios de respeito, colaboração e inclusão:

- ✅ Seja respeitoso com outros contribuidores
- ✅ Aceite críticas construtivas
- ✅ Foque no que é melhor para o projeto
- ✅ Mostre empatia com outros membros da comunidade

---

## 🚀 Como Começar

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub
# Depois clone seu fork:

git clone https://github.com/seu-usuario/pyblaze.git
cd pyblaze
```

### 2. Configurar Ambiente

```bash
# Instalar dependências
make install

# Ou manualmente:
uv sync
uv pip install -e .
```

### 3. Verificar que Tudo Funciona

```bash
# Executar todos os testes e verificações
make check

# Rodar o jogo
make run
```

---

## 💻 Processo de Desenvolvimento

### Workflow Recomendado

1. **Criar Branch**
   ```bash
   git checkout -b feat/minha-nova-feature
   # ou
   git checkout -b fix/corrigir-bug
   ```

2. **Desenvolver**
   - Escreva código seguindo os [padrões](#padrões-de-código)
   - Adicione testes para novas funcionalidades
   - Atualize documentação conforme necessário

3. **Testar Localmente**
   ```bash
   # Executar todas as verificações
   make check

   # Simular CI localmente
   make ci
   ```

4. **Commit**
   ```bash
   # Seguir Conventional Commits
   git add .
   git commit -m "feat(player): adiciona dash lateral"
   ```

5. **Push e Pull Request**
   ```bash
   git push origin feat/minha-nova-feature
   # Abrir PR no GitHub
   ```

---

## 🎨 Padrões de Código

### Python

O projeto segue rigorosas diretrizes de qualidade:

#### Leia as Guidelines

**OBRIGATÓRIO:** Antes de contribuir, leia:

- [Python Best Practices](guidelines/python_best_practices.md)
- [Git Conventions](guidelines/git_convection.md)

#### Resumo Rápido

```python
# ✅ BOM
from typing import Final

MAX_SPEED: Final[int] = 10

def calculate_damage(base_damage: int, multiplier: float) -> int:
    """Calcula dano com multiplicador."""
    return int(base_damage * multiplier)

# ❌ RUIM
MAX_SPEED = 10  # Sem type hint

def calculate_damage(base_damage, multiplier):  # Sem tipos
    print(base_damage * multiplier)  # Usando print!
    return base_damage * multiplier
```

#### Checklist de Qualidade

Antes de fazer commit:

- [ ] ✅ Type hints em todas as funções públicas
- [ ] ✅ Docstrings em classes e funções públicas
- [ ] ✅ Sem uso de `print()` (use `logging`)
- [ ] ✅ Sem magic numbers (use `settings.py`)
- [ ] ✅ `ruff format` executado
- [ ] ✅ `ruff check` sem warnings
- [ ] ✅ `mypy` sem erros
- [ ] ✅ Testes passando

### Ferramentas

```bash
# Formatação automática
make format

# Verificar qualidade
make lint

# Type checking
make type-check

# Tudo de uma vez
make check
```

---

## 📝 Commits e Pull Requests

### Conventional Commits

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Features
git commit -m "feat(player): adiciona duplo pulo"
git commit -m "feat(enemies): novo inimigo voador"

# Fixes
git commit -m "fix(physics): corrige colisão em rampas"
git commit -m "fix(camera): remove jittering"

# Refatoração
git commit -m "refactor(systems): extrai HUD para módulo separado"

# Documentação
git commit -m "docs(readme): adiciona seção de instalação"

# Testes
git commit -m "test(player): adiciona testes de state machine"

# Chores
git commit -m "chore(deps): atualiza pygame-ce para 2.5.2"
```

### Tipos de Commit

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova funcionalidade | `feat(enemies): adiciona boss` |
| `fix` | Correção de bug | `fix(player): corrige pulo duplo` |
| `docs` | Documentação | `docs(api): atualiza docstrings` |
| `refactor` | Refatoração | `refactor(camera): simplifica lerp` |
| `test` | Testes | `test(physics): adiciona edge cases` |
| `chore` | Manutenção | `chore(ci): atualiza workflow` |
| `perf` | Performance | `perf(rendering): otimiza sprites` |
| `style` | Formatação | `style: aplica black` |

### Pull Requests

#### Template de PR

```markdown
## Descrição

[Descreva o que este PR faz]

## Tipo de Mudança

- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist

- [ ] Código segue os padrões do projeto
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] `make check` passa sem erros
- [ ] Commits seguem Conventional Commits

## Screenshots/GIFs

[Se aplicável]

## Testes

[Como testar esta mudança]
```

---

## ✅ Testes

### Escrever Testes

Todo novo código deve ter testes:

```python
# tests/unit/test_nova_feature.py

import pytest
from pyblaze.entities.player import Player

def test_player_dash(pygame_headless):
    """Testa que o dash aumenta velocidade temporariamente."""
    # Arrange
    player = Player(x=100, y=100)
    initial_speed = player.vx

    # Act
    player.dash()

    # Assert
    assert player.vx > initial_speed
    assert player.is_dashing is True
```

### Executar Testes

```bash
# Todos os testes
make test

# Com cobertura
make test-cov

# Teste específico
uv run pytest tests/unit/test_player.py -v

# Teste específico com função
uv run pytest tests/unit/test_player.py::test_player_dash -v
```

### Cobertura

- Foque em **lógica crítica** (física, state machine, colisões)
- Não é necessário 100% de cobertura
- Testes de integração são bem-vindos

---

## 📚 Documentação

### Quando Atualizar

Atualize documentação quando:

- Adicionar nova feature
- Mudar comportamento existente
- Adicionar novos comandos/scripts
- Corrigir erros na documentação

### Arquivos de Documentação

```
docs/
├── INDEX.md                  # Atualizar para novas guidelines
├── CONTRIBUTING.md           # Este arquivo
├── LESSONS_LEARNED.md        # Adicionar problemas encontrados
├── PROJETO_COMPLETO.md       # Atualizar métricas/features
├── QUICK_REFERENCE.md        # Adicionar comandos novos
├── guidelines/               # Adicionar novos padrões
└── prompts/                  # Atualizar prompts de IA
```

### README.md

Ao adicionar features que impactam usuários, atualize:

- Características
- Como usar
- Screenshots (se visual)
- Métricas

### Docstrings

```python
def calculate_trajectory(
    initial_velocity: float,
    angle: float,
    gravity: float = 9.8
) -> tuple[float, float]:
    """
    Calcula trajetória parabólica.

    Args:
        initial_velocity: Velocidade inicial em m/s
        angle: Ângulo de lançamento em graus
        gravity: Aceleração gravitacional (padrão: 9.8 m/s²)

    Returns:
        Tupla (distância, altura_máxima) em metros

    Example:
        >>> calculate_trajectory(10.0, 45.0)
        (10.2, 2.55)
    """
    ...
```

---

## 🐛 Reportar Bugs

### Template de Issue

```markdown
## Descrição do Bug

[Descreva claramente o bug]

## Passos para Reproduzir

1. Execute o jogo
2. Pressione X
3. Observe Y
4. Bug acontece

## Comportamento Esperado

[O que deveria acontecer]

## Comportamento Atual

[O que está acontecendo]

## Ambiente

- OS: [Windows 11 / Ubuntu 22.04 / macOS 13]
- Python: [3.12.0]
- pygame-ce: [2.5.7]

## Logs/Screenshots

[Anexar se aplicável]
```

---

## 💡 Sugerir Features

### Template de Feature Request

```markdown
## Descrição da Feature

[Descreva a feature proposta]

## Motivação

[Por que esta feature é útil?]

## Solução Proposta

[Como você imagina implementando?]

## Alternativas Consideradas

[Outras abordagens possíveis]

## Impacto

- [ ] Breaking change
- [ ] Nova dependência
- [ ] Mudança de performance
```

---

## 🎓 Primeiros Passos

### Issues para Iniciantes

Procure por labels:

- `good first issue` - Bom para começar
- `help wanted` - Ajuda bem-vinda
- `documentation` - Melhorias em docs
- `bug` - Correção de bugs

### Onde Contribuir

**Fácil:**
- Melhorar documentação
- Adicionar testes
- Corrigir typos
- Adicionar exemplos

**Médio:**
- Novos inimigos/itens
- Melhorias de gameplay
- Otimizações de performance
- Refatorações

**Avançado:**
- Sistema de save/load
- Multiplayer
- Level editor
- Novas engines/frameworks

---

## 🔄 Processo de Review

### O que Esperamos

1. **Código limpo** seguindo padrões
2. **Testes adequados** para mudanças
3. **Documentação atualizada**
4. **CI passando** (GitHub Actions)
5. **Commits bem descritos**

### Timeline

- **Review inicial:** 1-3 dias
- **Feedback:** Até 2 dias
- **Merge:** Após aprovação e CI verde

### Dicas para Aprovação Rápida

- ✅ PRs pequenos e focados
- ✅ Descrição clara
- ✅ Screenshots/GIFs quando aplicável
- ✅ Testes passando
- ✅ Sem conflitos com main

---

## 📞 Contato

### Dúvidas?

- Abra uma **Issue** para discussão
- Consulte a [documentação completa](INDEX.md)
- Veja [exemplos de código](../src/pyblaze/)

---

## 🏆 Reconhecimento

Contribuidores são reconhecidos:

- Seção de **Créditos** no README
- Menção nas **Release Notes**
- Co-autoria em commits (quando aplicável)

---

## 📜 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (uso educacional).

---

**Obrigado por contribuir com o PyBlaze! 🎮🚀**

*Desenvolvido com ❤️ pela comunidade*
