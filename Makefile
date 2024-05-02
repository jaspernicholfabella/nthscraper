# Makefile for this project (for ease of development)

.PHONY: build test lint

build:
	pip install .
test:
	python -m unittest discover -s tests -p "*.py"
lint:
	black .
