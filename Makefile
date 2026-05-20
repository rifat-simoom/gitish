.PHONY: help install install-dev test lint format clean build publish

help:
	@echo "Gitish - Development Commands"
	@echo ""
	@echo "  install       Install package"
	@echo "  install-dev   Install package with dev dependencies"
	@echo "  test          Run tests with coverage"
	@echo "  lint          Run linters (flake8, mypy)"
	@echo "  format        Format code with black and isort"
	@echo "  clean         Remove build artifacts"
	@echo "  build         Build distribution packages"
	@echo "  publish       Publish to PyPI (requires credentials)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest --cov=gitish --cov-report=term-missing --cov-report=html

lint:
	flake8 gitish tests
	mypy gitish

format:
	black gitish tests
	isort gitish tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	twine upload dist/*

.DEFAULT_GOAL := help
