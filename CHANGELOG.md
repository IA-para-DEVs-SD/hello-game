# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.1.0] - 2026-03-11

### ✨ Adicionado

#### Infraestrutura
- **Makefile** com 15+ comandos úteis para desenvolvimento
  - `make install` - Instala dependências
  - `make test` - Executa testes
  - `make check` - Executa todas as verificações
  - `make build-exe` - Cria executável standalone
  - `make ci` - Simula pipeline de CI localmente
  - Ver `make help` para lista completa

- **GitHub Actions CI/CD**
  - Pipeline automatizado em cada push/PR
  - Testes em múltiplas plataformas (Ubuntu, Windows, macOS)
  - Verificação de formatação, linting e type checking
  - Upload de cobertura para Codecov
  - Ver [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

- **Scripts de Build**
  - `build/build.py` - Cria executável com PyInstaller
  - `build/release.sh` - Automatiza processo de release
  - Suporte para Windows, Linux e macOS

- **Badges no README**
  - Python version
  - pygame-ce version
  - Testes passando
  - Type checking (mypy strict)
  - Code style (ruff)
  - CI status

#### Documentação
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Guia completo de contribuição
  - Processo de desenvolvimento
  - Padrões de código
  - Como escrever commits e PRs
  - Templates de issues e PRs
- **[CHANGELOG.md](CHANGELOG.md)** - Este arquivo

### 🔧 Melhorado

- **.gitignore** expandido e mais robusto
  - Cobertura completa de arquivos temporários
  - Suporte para build tools (PyInstaller)
  - Logs, saves e screenshots ignorados
  - Configurações de IDE

- **README.md** reestruturado
  - Seção de badges informativos
  - Comandos do Makefile documentados
  - Seção de Build e Distribuição
  - Informações sobre CI/CD

- **[PROJETO_COMPLETO.md](docs/PROJETO_COMPLETO.md)** atualizado
  - Novos comandos com Makefile
  - Seção de build de executável
  - Diferencial de "Infraestrutura Moderna"

### 📊 Métricas

- Arquivos de documentação: 10 → 12
- Scripts de automação: 0 → 2
- Comandos Make disponíveis: 0 → 15
- Plataformas CI: 0 → 3 (Ubuntu, Windows, macOS)

---

## [1.0.0] - 2026-03-11

### ✨ Release Inicial

#### Jogo Completo
- Jogo de plataforma 2D inspirado em Sonic the Hedgehog
- Fase completa com 4 zonas distintas
- Sistema de movimento com aceleração e sprint
- Pulo variável (curto/longo)
- Spin attack para combate
- Sistema de anéis e vidas
- Checkpoints de respawn
- Câmera suave com lerp
- HUD com contador de anéis, vidas e timer
- Telas de menu, game over e vitória

#### Elementos de Gameplay
- 28 anéis coletáveis
- 6 inimigos patrulheiros
- 4 checkpoints
- Rampas de aceleração
- Plataformas aéreas
- Abismos mortais
- Bandeira de chegada

#### Qualidade de Código
- **21 módulos** organizados em arquitetura limpa
- **~1500 linhas** de código Python
- **26 testes unitários** (100% passando)
- **Type hints completos** (mypy strict mode)
- **0 warnings** de linting (ruff)
- **60 FPS** estáveis
- Logging estruturado (sem prints)

#### Arquitetura
- Separação em camadas: Entities, Systems, Scenes
- State machine completa do player (9 estados)
- Sistema de física com gravidade e colisões AABB
- Câmera com suavização
- HUD modular

#### Documentação
- **[INDEX.md](docs/INDEX.md)** - Índice completo da documentação
- **[README.md](README.md)** - Guia do usuário
- **[PROJETO_COMPLETO.md](docs/PROJETO_COMPLETO.md)** - Resumo executivo
- **[LESSONS_LEARNED.md](docs/LESSONS_LEARNED.md)** - Lições aprendidas
- **[QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md)** - Referência rápida

#### Guidelines
- [git_convection.md](docs/guidelines/git_convection.md) - Padrões Git
- [python_best_practices.md](docs/guidelines/python_best_practices.md) - Python moderno
- [docker_best_practices.md](docs/guidelines/docker_best_practices.md) - Docker
- [product_requirements_document.md](docs/guidelines/product_requirements_document.md) - PRD
- [tech_spec.md](docs/guidelines/tech_spec.md) - Especificações técnicas
- [readme_writing_guide.md](docs/guidelines/readme_writing_guide.md) - Como escrever README

#### Stack Tecnológica
- Python 3.12
- pygame-ce 2.5+
- UV (gerenciador de pacotes)
- Ruff (linting e formatação)
- MyPy (type checking)
- pytest (testes)
- pytest-cov (cobertura)

---

## Tipos de Mudanças

- **✨ Adicionado** - Novas features
- **🔧 Melhorado** - Mudanças em features existentes
- **🐛 Corrigido** - Bug fixes
- **🗑️ Removido** - Features removidas
- **⚠️ Deprecated** - Features que serão removidas
- **🔒 Segurança** - Correções de segurança
- **📊 Métricas** - Métricas e estatísticas

---

## Links

- [Repositório](https://github.com/usuario/pyblaze)
- [Issues](https://github.com/usuario/pyblaze/issues)
- [Pull Requests](https://github.com/usuario/pyblaze/pulls)
- [Releases](https://github.com/usuario/pyblaze/releases)
