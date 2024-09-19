# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = source $(VENV_DIR)/bin/activate

# Targets
.PHONY: all venv install test clean

all: venv install

venv:
	python3 -m venv $(VENV_DIR)

install:
	pip3 install --upgrade pip
	pip3 install -r pip-requirements.txt -r dev-requirements.txt

test: install
	pytest

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -exec rm -f {} +
	find . -type f -name "*.log" -exec rm -f {} +
	find . -type f -name "*.csv" -exec rm -f {} +
	find . -type f -name "*.db" -exec rm -f {} +

freeze:
	pip3 freeze > requirements.txt
