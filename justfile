# Define o python da venv (ajuste o caminho se precisar)

# Comando base para rodar manage.py
manage := "uv run .venv/bin/python3.13 manage.py"

run:
    just manage runserver 8000

debug:
    just manage runserver

remigrate:
    rm -rf auctions/migrations/*
    just makemigrations auctions
    just redb

redb:
    rm -f db.sqlite3
    just migrate
    just populate

populate:
    just manage populate

create_superuser:
    just manage createsuperuser

manage *args:
    {{manage}} {{args}}

makemigrations *args:
    just manage makemigrations {{args}}

migrate *args:
    just manage migrate {{args}}

collectstatic *args:
    just manage collectstatic {{args}}

fmt:
    .venv/bin/ruff format .

build:
    uv sync
    just migrate
    just collectstatic --no-input
