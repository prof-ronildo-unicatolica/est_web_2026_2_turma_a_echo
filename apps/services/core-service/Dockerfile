FROM python:3.12-slim

WORKDIR /app

# Instala as dependencias no Python do sistema (sem virtualenv). Via ENV, e nao
# via `poetry config`, para valer tambem para o usuario sem privilegios que roda
# os comandos `poetry run` do docker-compose.
ENV POETRY_VIRTUALENVS_CREATE=false

# Dependencias do sistema e Poetry numa unica camada
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry==1.8.2

# Copia apenas os arquivos de configuracao de dependencias
COPY pyproject.toml poetry.lock poetry.toml ./

RUN poetry install --no-interaction --no-ansi --without dev

# Usuario sem privilegios: um processo comprometido na aplicacao nao vira root
# no conteiner.
RUN useradd --create-home --uid 1000 app

# Copia somente os arquivos necessarios para executar a aplicacao
COPY --chown=app:app app/ ./app/
COPY --chown=app:app alembic/ ./alembic/
COPY --chown=app:app alembic.ini ./

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
