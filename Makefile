ROOT_DIR := '/'
REQUIREMNTS := 'requirements.txt'
PIP := $(PIP)
PYTHON := $(PYTHON)
HOST := $(HOST)
PORT := $(PORT)


run:
	@$(PYTHON) manage.py runserver $(HOST):$(PORT)

test:
	@$(PYTHON) manage.py test

check-code:
	@ flake8

check-deploy:
	@ $(PYTHON) manage.py check --deploy

mm:
	@ $(PYTHON) manage.py makemigrations
	@ $(PYTHON) manage.py migrate

build_env:
	@ docker-compose build

run_env:
	@ docker-compose up
