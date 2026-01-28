.PHONY: help install install-dev test test-cov lint typecheck format clean run-example run-async-example build check-all

help:
	@echo "py-euroleague development commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install package dependencies"
	@echo "  make install-dev  Install package with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo "  make lint         Run linter (ruff)"
	@echo "  make typecheck    Run type checker (mypy)"
	@echo "  make format       Format code with ruff"
	@echo ""
	@echo "Examples:"
	@echo "  make run-example       Run basic usage example"
	@echo "  make run-async-example Run async usage example"
	@echo ""
	@echo "Release:"
	@echo "  make build        Build package"
	@echo "  make check-all    Run all checks (lint, typecheck, test)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove caches"

install:
	poetry install --only main

install-dev:
	poetry install

test: install-dev
	poetry run pytest

test-cov: install-dev
	poetry run pytest --cov=euroleague --cov-report=term-missing

lint: install-dev
	poetry run ruff check src/ tests/

typecheck: install-dev
	poetry run mypy src/euroleague

format: install-dev
	poetry run ruff format src/ tests/
	poetry run ruff check --fix src/ tests/

run-example: install
	poetry run python examples/basic_usage.py

run-async-example: install
	poetry run python examples/async_example.py

build: clean
	poetry build

check-all: lint typecheck test
	@echo "All checks passed!"

clean:
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf src/*.egg-info
	rm -rf dist/
	rm -rf build/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Cleaned up."
