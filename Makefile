.PHONY: test lint

test:
	python3 -m pytest

lint:
	python3 -m ruff check .
