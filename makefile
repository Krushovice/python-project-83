# переменные разработки
PORT ?= 8000
DB_NAME = pages
LOCAL_DB_USER = krushovice


install:
	poetry install

build-db: db-reset schema-data-load

db-create:
	createdb $(DB_NAME)

db-drop:
	dropdb $(DB_NAME)

db-reset:
	dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

dbs-show:
	psql -l

db-connect:
	psql -d $(DB_NAME)

db-dev-setup: db-reset schema-data-load

schema-data-load:
	psql $(DB_NAME) < database.sql


dev-server-run:
	poetry run flask --app page_analyzer:app run

render:
	PGPASSWORD=IPj89bzlZKve7tUZVyFcrUck1amTZ8xb psql -h dpg-cknq6f9rfc9c739si3i0-a.oregon-postgres.render.com -U krushovice pages_j6gj

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build: #  Сборка пакета
	./build.sh

lint:
	poetry run flake8 page_analuzer

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analuzer --cov-report xml tests/

.PHONY: install
