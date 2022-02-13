.DEFAULT_GOAL := all

project_dirs = aiosendgrid
tests_dirs = tests

.PHONY: install
install:
	poetry install --no-root -E helpers

.PHONY: format
format:
	autoflake --recursive --remove-all-unused-imports --remove-unused-variables $(project_dirs) $(tests_dirs)
	black $(project_dirs) $(tests_dirs)
	isort $(project_dirs) $(tests_dirs)

.PHONY: check
check:
	black $(project_dirs) $(tests_dirs) --check --diff
	isort $(project_dirs) $(tests_dirs) --check-only --df
	flake8 $(project_dirs) $(tests_dirs)
	mypy $(project_dirs)

.PHONY: test
test:
	pytest

.PHONY: all
all: check test

.PHONY: build
build:
	poetry build

.PHONY: publish
publish: build
	poetry publish

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -f .coverage
	rm -f .coverage.*
	rm -rf dist
	rm -rf coverage.xml
