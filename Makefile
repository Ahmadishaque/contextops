.PHONY: install lint typecheck test format

install:
	pip install -r requirements.txt

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app

test:
	pytest
