install:
	poetry install

build: #  Сборка пакета
	poetry build

publish:
	poetry publish --dry-run
make
package-install:
	pip install --user --force-reinstall dist/*.whl

lint:
	poetry run flake8 app

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml tests/

.PHONY: install build publish package-install lint check test-coverage

dev:
	poetry run flask --app page_analyzer: app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
