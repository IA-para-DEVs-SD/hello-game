# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.7.1] - 2026-03-27

### ✨ Adicionado

#### Sistema Completo de Sprites Visuais
- **AssetManager** - Gerenciador centralizado de sprites com cache automático
  - Carregamento inteligente de sprites
  - Fallback para formas geométricas
  - Suporte a spritesheets e sprites únicos
  - Sistema de prioridade (procedural → avançado → básico)

- **Sprites Avançados** - Sprites com efeitos visuais profissionais
  - Player estilo Sonic com gradientes radiais e sombras
  - Enemy vermelho com olhos amarelos brilhantes
  - Ring dourado em forma de anel com brilho
  - Checkpoints com bandeiras animadas
  - Platform tiles com textura de terra e grama
  - Spritesheet do player com 4 frames de animação

- **Sistema de Sprites Procedurais** - Geração infinita de sprites únicos
  - 21 máscaras customizadas (personagens, criaturas, objetos, cenário)
  - Gerador procedural com paletas HSV aleatórias
  - Espelhamento automático e contornos
  - 100+ sprites gerados automaticamente
  - Variações infinitas a cada execução

#### Ferramentas de Desenvolvimento (8 scripts)
- `generate_sprites.py` - Gerador de sprites básicos
- `generate_advanced_sprites.py` - Gerador de sprites com efeitos
- `procedural_sprite_generator.py` - Gerador procedural base
- `generate_all_sprites.py` - Gera todos os sprites de uma vez
- `custom_masks.py` - Biblioteca de 21 máscaras
- `switch_sprites.py` - Alternador entre sprites normais/procedurais
- `sprite_viewer.py` - Visualizador interativo de sprites
- `create_player_spritesheet.py` - Cria spritesheet do player

#### Documentação Extensiva (4 guias, 3000+ linhas)
- **SPRITE_GUIDE.md** (900+ linhas) - Guia completo de criação de sprites
  - Técnicas de desenho com pygame
  - Gradientes, sombras e brilhos
  - Criação de spritesheets
  - Integração nas entidades
  - Animações por estado
  - Troubleshooting completo

- **SPRITES_IMPLEMENTATION.md** - Documentação técnica da implementação
  - Arquitetura do AssetManager
  - Sistema de cache
  - Integração nas entidades
  - Fluxo de carregamento

- **SPRITES_SUMMARY.md** - Resumo executivo do sistema
  - Estatísticas e métricas
  - Como usar as ferramentas
  - Estrutura de arquivos
  - Guia rápido

- **PROCEDURAL_SPRITES.md** - Sistema de geração procedural
  - Como funciona o gerador
  - Criando máscaras customizadas
  - Paletas de cores HSV
  - Exemplos práticos

#### Hooks de Automação (6 hooks)
- `auto-test-on-save` - Executa testes ao editar código
- `verify-game-startup` - Verifica se jogo inicia em mudanças críticas
- `update-docs-reminder` - Lembra de atualizar documentação
- `quality-check-on-finish` - Formata código ao finalizar
- `final-test-check` - Executa testes completos ao finalizar
- `suggest-commit` - Sugere commits ao terminar trabalho

### 🔧 Melhorado

#### Entidades Atualizadas
- **Player** - Sistema de animação com 4 frames
  - Frame 0: Idle (parado)
  - Frames 1-2: Running (correndo)
  - Frame 3: Jumping/Spin (pulando)
  - Espelhamento horizontal baseado na direção
  - Integração com AssetManager

- **Enemy** - Sprite avançado com efeitos visuais
- **Ring** - Rotação suave do sprite
- **Checkpoint** - Sprites diferentes para ativo/inativo

#### Estrutura do Projeto
- Pasta `assets/` criada para sprites
- Pasta `tools/` criada para scripts de desenvolvimento
- Pasta `.kiro/hooks/` criada para automação
- Documentação reorganizada em `docs/`

### 📊 Estatísticas

- **Sprites criados:** 112+ (6 básicos + 6 avançados + 100+ procedurais)
- **Ferramentas:** 8 scripts Python
- **Documentação:** 4 guias (3000+ linhas)
- **Máscaras:** 21 tipos diferentes
- **Hooks:** 6 automações
- **Testes:** 26/26 passando (100%)
- **Cobertura:** 62% (acima dos 30% requeridos)

### 🎨 Recursos Visuais

- Sprites estilo Sonic com gradientes e sombras
- Sistema de animação fluido
- Efeitos de brilho e volume
- Paletas de cores harmônicas
- Geração procedural infinita

---

## [Unreleased] - 2026-03-26

### ♻️ Refatorado

#### Reorganização Completa da Documentação
- **Criada estrutura `.kiro/`** para especificações e convenções
  - `.kiro/specs/` - Especificações (O QUÊ fazer)
    - `prd.md` - Product Requirements Document
    - `tech_spec.md` - Especificações técnicas
  - `.kiro/steering/` - Convenções (COMO fazer)
    - `git_convention.md` - Convenções Git e GitHub CLI
    - `python_convention.md` - Padrões Python
    - `docker_convention.md` - Padrões Docker
    - `documentation_convention.md` - Guia de documentação completo
    - `game_agent_convention.md` - Convenções para agentes IA

- **Padronização de nomes**
  - Todos os arquivos de convenção agora usam sufixo `_convention.md`
  - Nomes simplificados: `prd.md` (antes: `product_requirements_document.md`)
  - Correção de typo: `git_convention.md` (antes: `git_convection.md`)

- **Pasta `docs/` limpa**
  - Mantém apenas documentação de referência
  - Removidas pastas `docs/guidelines/` e `docs/prompts/`
  - Estrutura mais clara e navegável

### ✨ Adicionado

#### Convenções Git (`.kiro/steering/git_convention.md`)
- **Formato de commit com colchetes**: `[tipo]: Descrição`
  - Substitui formato com parênteses por simplicidade
  - Primeira letra maiúscula obrigatória
- **Automação completa com GitHub CLI** para org IA-para-DEVs-SD
  - Comandos para trabalhar com múltiplos grupos (1-6)
  - Listar, criar e clonar repositórios
  - Gerenciar Projects/Boards
  - Criar e gerenciar Issues e PRs
  - **Criar cards diretamente nos boards** com GraphQL
  - Script helper `create-card.sh` para criação rápida
  - Workflow completo end-to-end
  - Templates de Issue e PR prontos
  - 10 dicas práticas para LLMs

#### Guia de Documentação (`.kiro/steering/documentation_convention.md`)
- **Guia completo** expandido do antigo `readme_writing_guide.md`
- Cobre todos os tipos de documentação:
  - README.md (com exemplos para jogos e APIs)
  - Documentação técnica (INDEX, PROJETO_COMPLETO, QUICK_REFERENCE, etc)
  - Guias e tutoriais
  - Especificações (PRD e Tech Spec)
  - Changelog (formato Keep a Changelog)
- **6 tipos de diagramas Mermaid** com exemplos práticos
- Boas práticas gerais (badges, tabelas, alertas, etc)
- Checklist de qualidade completo
- ~900 linhas de referência

### 🔧 Corrigido

- **README.md** - Atualizado para refletir nova estrutura
  - Seção "Estrutura do Projeto" atualizada
  - Links para `.kiro/specs/` e `.kiro/steering/`
  - Seção "Documentação" reorganizada
- **docs/INDEX.md** - Completamente reescrito
  - Reflete nova organização `.kiro/`
  - Links corrigidos para specs e conventions
  - Descrições atualizadas

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
