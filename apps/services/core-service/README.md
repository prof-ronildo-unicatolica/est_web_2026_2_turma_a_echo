# Core Service - Backend (FastAPI + PostgreSQL + MongoDB)

Este diretório contém o **Core Service**, a API principal do Sistema de Reservas de Rede Hoteleira, desenvolvida em **FastAPI** (Python).

Atualmente, o projeto inclui a modelagem relacional do domínio hoteleiro (`Cidade` 1:N `Hotel`), autenticação JWT com controle de acesso por perfil (RBAC) e a estrutura institucional de apresentação da equipe (`Echo`) em bancos relacional (PostgreSQL via SQLAlchemy e Alembic) e NoSQL (MongoDB via Motor).

---

## Tecnologias e Dependências

* **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) (assíncrono e de alto desempenho).
* **Banco de Dados Relacional**: PostgreSQL (gerenciado via SQLAlchemy ORM).
* **Versionamento de Banco**: Alembic (gerencia migrações e seeds).
* **Banco de Dados NoSQL**: MongoDB (acessado assincronamente através da biblioteca Motor).
* **Validação de Dados**: Pydantic e Pydantic Settings (carrega variáveis do `.env`).
* **Segurança/Criptografia**: bcrypt (hash de senhas) e PyJWT (tokens de acesso).

---

## Arquitetura da Trilha Cidade e Hotel (Relação 1:N)

A modelagem entre `Cidade` e `Hotel` implementa um relacionamento **1:N (Um-para-Muitos)**:

1. **Models (`app/models/hotel.py`)**:
   * Uma `Cidade` possui vários hotéis (`hoteis: Mapped[List["Hotel"]] = relationship(..., back_populates="cidade")`).
   * A chave estrangeira (`cidade_id`) reside do lado **N** (na tabela `hoteis`, apontando para `cidades.id` com `ondelete="CASCADE"`).
2. **Schemas Assimétricos (`app/schemas/hotel.py`)**:
   * **Entrada (`HotelCreateSchema`)**: recebe apenas `cidade_id: UUID`, `nome: str` e `estrelas: int` (1 a 5), evitando ambiguidade entre referenciar uma cidade existente ou criar outra.
   * **Saída (`HotelResponseSchema`)**: devolve o objeto `cidade: CidadeResponseSchema` aninhado, permitindo que o frontend exiba o nome da cidade sem requisições adicionais.
3. **Repositories (`app/repositories/hotel_repository.py`)**:
   * Utiliza `joinedload(Hotel.cidade)` nas consultas para eliminar o problema de *N+1 queries* ao listar hotéis.
4. **Services (`app/services/cidade_service.py` e `hotel_service.py`)**:
   * Concentram as regras de negócio (normalização de espaços, unicidade do nome de cidade e validação de existência da cidade antes de criar ou atualizar um hotel).

---

## Como Executar o Backend Localmente

### 1. Pré-requisitos
Certifique-se de que os containers do banco de dados estejam rodando na raiz do projeto:
```bash
# Na raiz do monorepo:
docker compose up -d
```

### 2. Configurar o Arquivo de Variáveis (.env)
Duplique o arquivo de modelo `env_example` com o nome `.env`:
* **Linux/macOS**: `cp env_example .env`
* **Windows (PowerShell)**: `copy env_example .env`

---

### 3. Instalação e Execução

#### Opção A: Com Virtualenv Padrão (`venv`)
1. **Criar e Ativar Ambiente Virtual**:
   * No Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * No Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
2. **Instalar Dependências**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Rodar Migrações e Seeds (Alembic)**:
   ```bash
   alembic upgrade head
   ```
4. **Executar o Servidor**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

#### Opção B: Com Poetry
1. **Instalar e Ativar Ambiente**:
   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   poetry shell
   ```
2. **Rodar Migrações e Seeds (Alembic)**:
   ```bash
   poetry run alembic upgrade head
   ```
3. **Executar o Servidor**:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```

---

## Rotas Disponíveis (Endpoints)

Após iniciar o servidor, acesse a documentação interativa oficial do Swagger em **`http://localhost:8000/docs`**.

| Método | Rota | Acesso | O que faz |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | público | Boas-vindas |
| `GET` | `/api/v1/health` | público | Testa PostgreSQL e MongoDB (503 se algum cair) |
| `GET` | `/api/v1/sobre` | público | Equipe, professor, disciplinas e stacks |
| `GET` | `/api/v1/sobre/stacks` | público | Lista as stacks tecnológicas e linguagens |
| `POST` | `/api/v1/auth/register` | público | Cadastra usuário comum |
| `POST` | `/api/v1/auth/login` | público | Devolve o JWT |
| `GET` | `/api/v1/auth/me` | autenticado | Perfil do usuário do token |
| `POST` / `GET` | `/api/v1/cidades` | público | Cria e lista cidades |
| `GET` | `/api/v1/cidades/{id}` | público | Busca uma cidade pelo identificador |
| `GET` | `/api/v1/hoteis?cidade_id=` | público | Lista hotéis com a cidade aninhada, com filtro opcional |
| `GET` | `/api/v1/hoteis/{id}` | público | Busca um hotel pelo identificador |
| `POST` / `PUT` / `DELETE` | `/api/v1/hoteis` | admin | Cria, altera e exclui hotéis |

---

## Testes e Lint

Os testes usam SQLite em memória e dublês para MongoDB e RabbitMQ: não precisam de nenhum serviço externo em execução.
As variáveis obrigatórias do `Settings` precisam existir (o `.env` local basta).

```bash
pytest -q                            # suíte inteira
pytest tests/test_hotel_service.py -q # módulo específico
ruff check .                         # verificação estática de lint
ruff format --check .                # verificação de formatação
```

O CI (`.github/workflows/ci.yml`) roda `ruff check` e `pytest` em todo PR para a `develop`.

---

## Estrutura de Diretórios Interna

```text
├── alembic/                  # Configurações e scripts de migração do banco relacional
│   └── versions/             # Histórico de alterações e migrações (001, 002, 003)
├── app/
│   ├── api/
│   │   ├── deps.py           # Dependências de autenticação e autorização (RBAC)
│   │   └── v1/               # Controladores e Rotas da API (auth, cidades, health, hoteis, sobre)
│   ├── core/
│   │   ├── config.py         # Variáveis e configurações obtidas do .env
│   │   ├── database.py       # Gerenciamento de conexões com Postgres e MongoDB
│   │   ├── security.py       # Hash bcrypt e emissão/validação de tokens JWT
│   │   ├── seed_mongo.py     # Script de inicialização de usuários no MongoDB
│   │   └── seed_postgres.py  # Script idempotente de seed para PostgreSQL
│   ├── models/               # Modelos ORM SQLAlchemy (Cidade, Hotel, Usuario, Tutorial)
│   ├── schemas/              # Schemas Pydantic de entrada e saída
│   ├── repositories/         # Camada de acesso a dados (queries SQLAlchemy)
│   ├── services/             # Regras de negócio (Auth, Cidade, Hotel, Tutorial)
│   └── main.py               # Inicializador do app FastAPI e eventos de ciclo de vida
├── tests/                    # Suíte de testes unitários e de integração (pytest)
├── env_example               # Template visível de variáveis de ambiente
├── pyproject.toml            # Arquivo de dependências e configuração do Poetry/Pytest/Ruff
└── requirements.txt          # Dependências fixadas sincronizadas com o poetry.lock
```
