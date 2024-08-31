.PHONY: venv install format lint

.DEFAULT_GOAL := lint

env:
	@echo "Creating virtual environment..."
	@python3 -m venv .venv

install:
	@echo "Upgrading pip..."
	@pip install --upgrade pip

	@echo "Installing pinned pip dependencies..."
	@pip install -r pip-requirements.txt

	@echo "Installing shared development dependencies..."
	@pip install -r dev-requirements.txt

format:
	@echo "Running black..."
	@black .

	@echo "Running isort..."
	@isort .

lint: format
	@echo "Running pylint..."
	@pylint .
