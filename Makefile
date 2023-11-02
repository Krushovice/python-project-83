# переменные разработки
PORT ?= 8000
DB_NAME = pages
LOCAL_DB_USER = krushovice


install:
	poetry install


db-connect:
	psql -d $(DB_NAME)


schema-data-load:
	psql $(DB_NAME) < database.sql


dev-server-run:
	export FLASK_ENV=development
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build: #  Сборка пакета
	./build.sh

lint:
	poetry run flake8 page_analyzer

.PHONY: install
