.PHONY: all format lint test tests integration_tests docker_tests help extended_tests

# Default target executed when no arguments are given to make.
all: help

######################
# LINTING AND FORMATTING
######################

# Define a variable for Python and notebook files.
PYTHON_FILES=.
MYPY_CACHE=.mypy_cache
lint format: PYTHON_FILES=.
lint_package: PYTHON_FILES=camel_database_agent
lint_tests: PYTHON_FILES=tests
lint_tests: MYPY_CACHE=.mypy_cache_test

lint lint_diff lint_package lint_tests:
	ruff -V
	mypy -V
	[ "$(PYTHON_FILES)" = "" ] || ruff check $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || ruff format $(PYTHON_FILES) --diff
	[ "$(PYTHON_FILES)" = "" ] || mkdir -p $(MYPY_CACHE) && mypy $(PYTHON_FILES) --cache-dir $(MYPY_CACHE)

format format_diff:
	[ "$(PYTHON_FILES)" = "" ] || ruff format $(PYTHON_FILES)
	[ "$(PYTHON_FILES)" = "" ] || ruff check --select I --fix $(PYTHON_FILES)

spell_check:
	codespell --toml pyproject.toml

spell_fix:
	codespell --toml pyproject.toml -w

check_imports: $(shell find camel_database_agent -name '*.py')
	python ./scripts/check_imports.py $^

test:
	pytest tests

######################
# HELP
######################

help:
	@echo '----'
	@echo 'check_imports				- check imports'
	@echo 'format                       - run code formatters'
	@echo 'lint                         - run linters'
	@echo 'tests                        - run unit tests'