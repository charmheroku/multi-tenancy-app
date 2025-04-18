lint:
	flake8 src

isort:
	isort src

type-check:
	mypy src

run:
	 uvicorn src.main:app --reload

init:
	PYTHONPATH=src aerich init -t adapters.database.db_config.TORTOISE_ORM

init-db:
	PYTHONPATH=src aerich init-db

migrate:
	PYTHONPATH=src aerich migrate

upgrade:
	PYTHONPATH=src aerich upgrade
