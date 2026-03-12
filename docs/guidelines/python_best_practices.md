# Python Best Practices — Guia de Boas Práticas de Programação

> **Público-alvo:** Este documento é destinado a agentes de IA e desenvolvedores Python. Siga estas regras **sempre**, salvo indicação explícita do mantenedor do projeto. O objetivo é garantir código limpo, legível, testável e pronto para produção.

---

## 1. Estilo e Formatação (PEP 8 + ferramentas modernas)

### Regras fundamentais

| Regra                        | Detalhe                                                              |
|------------------------------|----------------------------------------------------------------------|
| Indentação                   | **4 espaços** — nunca tabs                                           |
| Comprimento máximo de linha  | **88 caracteres** (padrão Black)                                     |
| Encoding                     | Sempre **UTF-8**                                                     |
| Fim de arquivo               | Sempre terminar com **uma linha em branco**                          |
| Imports                      | Um por linha, agrupados e ordenados                                  |
| Aspas                        | Consistente no projeto — preferir aspas duplas `"` (padrão Black)   |

### Ferramentas obrigatórias

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "UP", "B", "SIM"]

[tool.mypy]
strict = true
python_version = "3.11"
```

```bash
# Executar antes de qualquer commit
black .
ruff check . --fix
mypy .
```

### Ordem dos imports

```python
# 1. Biblioteca padrão
import os
import sys
from pathlib import Path
from typing import Any

# 2. Bibliotecas de terceiros
import numpy as np
import pandas as pd
from pydantic import BaseModel

# 3. Módulos internos do projeto
from myproject.core import settings
from myproject.utils import helpers
```

---

## 2. Nomenclatura

### Convenções obrigatórias

| Elemento              | Convenção              | Exemplo                           |
|-----------------------|------------------------|-----------------------------------|
| Variável / função     | `snake_case`           | `user_id`, `calculate_discount`   |
| Classe                | `PascalCase`           | `UserProfile`, `RecommendModel`   |
| Constante             | `UPPER_SNAKE_CASE`     | `MAX_RETRIES`, `DEFAULT_TIMEOUT`  |
| Módulo / arquivo      | `snake_case`           | `feature_store.py`, `train.py`    |
| Pacote / diretório    | `snake_case` sem hífen | `data_pipeline/`, `model_utils/`  |
| Variável privada      | `_prefixo_underscore`  | `_cache`, `_internal_state`       |
| "Dunder" (especial)   | `__nome__`             | `__init__`, `__repr__`            |

### Boas práticas de nomenclatura

```python
# ✅ Correto — nomes descritivos e intencionais
def calculate_user_churn_probability(user_id: int, lookback_days: int = 30) -> float:
    ...

MAX_RETRY_ATTEMPTS = 3
is_active_user = True
user_purchase_history: list[dict[str, Any]] = []

# ❌ Errado — nomes vagos, abreviações obscuras
def calc(u, d):
    ...

x = 3
flag = True
lst = []
```

---

## 3. Type Hints (Tipagem Estática)

### Regra geral

**Todo código novo deve ser totalmente tipado.** Use `mypy --strict` para validar.

```python
# ✅ Correto
def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    ...

def process_batch(items: list[str], max_size: int = 100) -> list[str]:
    ...

# ❌ Errado — sem tipagem
def get_user_by_id(user_id):
    ...
```

### Tipos modernos (Python 3.10+)

```python
# Prefira a sintaxe moderna ao invés dos imports do typing
# ✅ Moderno
def find(value: str | None) -> list[str] | None: ...

# ❌ Legado (evitar em Python 3.10+)
from typing import List, Optional, Union
def find(value: Optional[str]) -> Optional[List[str]]: ...
```

### Tipos úteis do módulo `typing`

```python
from typing import Any, Callable, TypeVar, Protocol, TypedDict, Final

# TypedDict para dicionários com estrutura conhecida
class UserRecord(TypedDict):
    id: int
    name: str
    email: str

# Final para constantes imutáveis
MAX_TOKENS: Final = 4096

# TypeVar para funções genéricas
T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## 4. Funções e Métodos

### Regras de design

- Uma função deve fazer **uma única coisa** (Princípio da Responsabilidade Única).
- Máximo de **20 linhas** por função. Se passar, considere extrair.
- Máximo de **4 parâmetros**. Se precisar de mais, use um objeto/dataclass.
- Prefira **retorno explícito** — evite efeitos colaterais desnecessários.
- Sempre adicionar **docstring** em funções públicas.

```python
# ✅ Correto
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calcula o preço final após aplicar o desconto.

    Args:
        price: Preço original do produto em reais.
        discount_rate: Taxa de desconto entre 0.0 e 1.0.

    Returns:
        Preço final após desconto.

    Raises:
        ValueError: Se discount_rate não estiver entre 0 e 1.
    """
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError(f"discount_rate deve ser entre 0 e 1, recebeu: {discount_rate}")
    return price * (1 - discount_rate)


# ❌ Errado — múltiplas responsabilidades, sem tipos, sem docstring
def process(p, d, save=False):
    r = p - (p * d)
    if save:
        with open("result.txt", "w") as f:
            f.write(str(r))
    return r
```

### Argumentos padrão mutáveis — armadilha clássica

```python
# ❌ NUNCA — lista mutável como default é compartilhada entre chamadas
def append_item(item: str, result: list = []) -> list:
    result.append(item)
    return result

# ✅ Correto — usar None e instanciar dentro da função
def append_item(item: str, result: list[str] | None = None) -> list[str]:
    if result is None:
        result = []
    result.append(item)
    return result
```

---

## 5. Classes e Dataclasses

### Preferir `dataclass` ou `Pydantic` para modelos de dados

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

# Para dados internos simples: dataclass
@dataclass
class TrainingConfig:
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 10
    feature_columns: list[str] = field(default_factory=list)

# Para validação de entrada/saída (API, configs): Pydantic
class PredictionRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="ID do usuário")
    n_recommendations: int = Field(default=10, ge=1, le=100)
    context: dict[str, Any] = Field(default_factory=dict)
```

### Implementar `__repr__` e `__str__` em classes customizadas

```python
class ModelArtifact:
    def __init__(self, name: str, version: str) -> None:
        self.name = name
        self.version = version

    def __repr__(self) -> str:
        return f"ModelArtifact(name={self.name!r}, version={self.version!r})"

    def __str__(self) -> str:
        return f"{self.name} v{self.version}"
```

---

## 6. Tratamento de Erros e Exceções

### Regras obrigatórias

- **Nunca** usar `except Exception` ou `except:` sem logar o erro.
- **Nunca** silenciar exceções com `pass` sem comentário justificado.
- Criar **exceções customizadas** para erros de domínio da aplicação.
- Usar `finally` para garantir liberação de recursos.

```python
# ✅ Correto — exceção específica + log + re-raise quando necessário
import logging

logger = logging.getLogger(__name__)

class PipelineError(Exception):
    """Erro base para falhas no pipeline de ML."""

class FeatureStoreConnectionError(PipelineError):
    """Falha ao conectar com o Feature Store."""


def fetch_features(user_id: int) -> dict[str, float]:
    try:
        return feature_store.get(user_id)
    except TimeoutError as e:
        logger.error("Timeout ao buscar features para user_id=%d: %s", user_id, e)
        raise FeatureStoreConnectionError(f"Timeout para user {user_id}") from e
    except KeyError:
        logger.warning("Features não encontradas para user_id=%d", user_id)
        return {}


# ❌ Errado — swallowing exceptions
def fetch_features(user_id):
    try:
        return feature_store.get(user_id)
    except:
        pass
```

### Context managers para recursos

```python
# ✅ Sempre usar with para arquivos, conexões e locks
with open("data.csv", encoding="utf-8") as f:
    content = f.read()

# ✅ Criar context managers customizados quando necessário
from contextlib import contextmanager

@contextmanager
def managed_db_connection(dsn: str):
    conn = connect(dsn)
    try:
        yield conn
    finally:
        conn.close()
```

---

## 7. Logging

### Configuração padrão

```python
import logging

# Configurar no entry point da aplicação (main.py, app.py)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)
```

### Regras de uso

```python
# ✅ Correto — usar % formatting (lazy evaluation, mais performático)
logger.info("Iniciando treinamento: model=%s, samples=%d", model_name, n_samples)
logger.error("Falha na predição para user_id=%d: %s", user_id, error)

# ❌ Errado — f-string sempre avaliada, mesmo se o log não for exibido
logger.info(f"Iniciando treinamento: model={model_name}, samples={n_samples}")

# Níveis corretos por situação:
logger.debug(...)    # detalhes de diagnóstico (dev apenas)
logger.info(...)     # eventos normais de negócio
logger.warning(...)  # situação inesperada mas recuperável
logger.error(...)    # falha em operação específica
logger.critical(...) # falha que pode derrubar a aplicação

# NUNCA usar print() em código de produção
```

---

## 8. Testes

### Estrutura de diretórios

```
project/
├── src/
│   └── myproject/
│       ├── core.py
│       └── utils.py
└── tests/
    ├── unit/
    │   ├── test_core.py
    │   └── test_utils.py
    ├── integration/
    │   └── test_pipeline.py
    └── conftest.py
```

### Regras de testes

- Um teste deve validar **um único comportamento**.
- Nome do teste: `test_<funcao>_<cenario>_<resultado_esperado>`.
- Usar **fixtures** para setup/teardown repetitivo.
- Usar **mocks** para isolar dependências externas (I/O, APIs, banco).
- Cobertura mínima: **80%** para código de produção.

```python
import pytest
from unittest.mock import MagicMock, patch

# ✅ Correto — nomenclatura clara + arrange/act/assert
def test_calculate_discount_valid_rate_returns_discounted_price():
    # Arrange
    price = 100.0
    discount_rate = 0.2

    # Act
    result = calculate_discount(price, discount_rate)

    # Assert
    assert result == 80.0


def test_calculate_discount_invalid_rate_raises_value_error():
    with pytest.raises(ValueError, match="discount_rate deve ser entre 0 e 1"):
        calculate_discount(price=100.0, discount_rate=1.5)


# Fixture para setup compartilhado
@pytest.fixture
def mock_feature_store():
    store = MagicMock()
    store.get.return_value = {"age": 25.0, "spend_30d": 450.0}
    return store


def test_fetch_features_returns_dict_on_success(mock_feature_store):
    with patch("myproject.pipeline.feature_store", mock_feature_store):
        result = fetch_features(user_id=42)
    assert "age" in result
    mock_feature_store.get.assert_called_once_with(42)
```

### Configuração do pytest

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src --cov-report=term-missing"

[tool.coverage.report]
fail_under = 80
```

---

## 9. Gerenciamento de Dependências

### Usar `uv` (moderno) ou `poetry`

```bash
# uv — mais rápido e recomendado para projetos novos
uv init myproject
uv add pandas numpy scikit-learn
uv add --dev pytest black ruff mypy

# poetry (legado, ainda amplamente usado)
poetry add pandas numpy
poetry add --group dev pytest black ruff mypy
```

### pyproject.toml — estrutura mínima

```toml
[project]
name = "myproject"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "black>=24.0.0",
    "ruff>=0.4.0",
    "mypy>=1.9.0",
]
```

### Regras de dependências

- **Nunca** commitar `requirements.txt` gerado manualmente em projetos com `uv`/`poetry`.
- **Sempre** fixar versões mínimas (`>=`) em bibliotecas, versões exatas (`==`) apenas quando crítico.
- Separar dependências de **produção** e **desenvolvimento**.
- Commitar sempre o **lockfile** (`uv.lock` ou `poetry.lock`).

---

## 10. Estrutura de Projeto

### Layout recomendado (src layout)

```
myproject/
├── pyproject.toml
├── README.md
├── .env.example             # variáveis de ambiente — nunca commitar .env
├── .gitignore
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py          # entry point
│       ├── config.py        # settings via pydantic-settings
│       ├── models/          # modelos de dados (Pydantic, dataclasses)
│       ├── services/        # lógica de negócio
│       ├── repositories/    # acesso a dados (DB, APIs, storage)
│       └── utils/           # funções utilitárias puras
└── tests/
    ├── conftest.py
    ├── unit/
    └── integration/
```

### Configuração via variáveis de ambiente

```python
# ✅ Usar pydantic-settings para configuração tipada e validada
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    project_name: str = "myproject"
    debug: bool = False
    database_url: str
    gcp_project_id: str
    vertex_ai_region: str = "us-central1"
    bigquery_dataset: str

settings = Settings()  # Lê automaticamente do .env ou ambiente

# ❌ Nunca hardcodar segredos ou configs de ambiente no código
GCP_PROJECT = "my-real-project-id"  # NUNCA
```

---

## 11. Performance e Código Pythônico

### Prefira expressões nativas do Python

```python
# ✅ List comprehension ao invés de loop + append
squares = [x**2 for x in range(100) if x % 2 == 0]

# ✅ Generator expression para grandes volumes (lazy evaluation)
total = sum(x**2 for x in range(1_000_000))

# ✅ Dict comprehension
user_map = {u["id"]: u["name"] for u in users}

# ✅ Walrus operator (:=) para evitar dupla avaliação
if chunk := file.read(8192):
    process(chunk)

# ✅ Unpacking
first, *rest = [1, 2, 3, 4, 5]
a, b = b, a  # swap sem variável temporária

# ✅ enumerate ao invés de range(len(...))
for idx, item in enumerate(items, start=1):
    print(f"{idx}. {item}")

# ✅ zip para iterar dois iteráveis em paralelo
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

### Evitar antipadrões comuns

```python
# ❌ Comparação com True/False/None explícita
if is_active == True: ...    # ❌
if value == None: ...        # ❌

# ✅ Forma Pythônica
if is_active: ...
if value is None: ...

# ❌ Concatenação de strings em loop (O(n²))
result = ""
for word in words:
    result += word + " "

# ✅ join é O(n)
result = " ".join(words)

# ❌ Catch genérico
try:
    ...
except Exception:
    pass

# ❌ Importar tudo de um módulo
from os.path import *
```

---

## 12. Referência Rápida

```
FORMATAÇÃO:     black + ruff + mypy antes de todo commit
TIPAGEM:        toda função pública deve ter type hints completos
NOMENCLATURA:   snake_case funções/vars | PascalCase classes | UPPER_SNAKE_CASE constantes
FUNÇÕES:        1 responsabilidade | máx. 20 linhas | máx. 4 parâmetros | docstring obrigatória
ERROS:          exceções específicas | nunca silenciar | sempre logar
LOGGING:        logger.info(...) com % formatting | nunca print() em produção
TESTES:         arrange/act/assert | nome descritivo | mock dependências externas | cobertura ≥ 80%
DEPENDÊNCIAS:   uv ou poetry | lockfile no git | separar prod de dev | nunca hardcodar segredos
ESTRUTURA:      src layout | config via pydantic-settings | .env nunca no git

NUNCA:
  - Argumento padrão mutável (def f(x, lst=[]))
  - except: sem log
  - print() em produção
  - Segredos no código fonte
  - Imports com * (from module import *)
  - Commits sem tipos + mypy passando
```