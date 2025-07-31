# Define o python da venv (ajuste o caminho se precisar)

# Comando base para rodar manage.py
manage := "uv run .venv/bin/python3.13 manage.py"

start:
    {{manage}} runserver

run:
    {{manage}} runserver 0.0.0.0:8000

debug:
    {{manage}} runserver

remigrate:
    rm -rf auctions/migrations/*
    just makemigrations auctions
    just redb

redb:
    rm -f db.sqlite3
    just migrate

create_sample_data:
    just manage create_sample_data

manage *args:
    {{manage}} {{args}}

makemigrations *args:
    just manage makemigrations {{args}}

migrate *args:
    just manage migrate {{args}}

collectstatic *args:
    just manage collectstatic {{args}}

fmt:
    ruff format .

build:
    uv sync
    just migrate
    just collectstatic --no-input
