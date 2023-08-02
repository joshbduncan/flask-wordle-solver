VENV:=venv
BIN:=$(VENV)/bin
PWD := $(realpath $(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

.DEFAULT_GOAL := help
.PHONY: help
##@ General
help: ## Display this help section
	@echo $(MAKEFILE_LIST)
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

venv: requirements.txt  ## build a virtual environment for development
	python -m venv $(VENV)
	$(BIN)/pip install -r requirements-dev.txt

##@ Development
cleanup: lint typing ## format, lint, and type check
	@echo "📝 cleanup..."
	$(BIN)/isort app.py flask_wordle_solver
	$(BIN)/black app.py flask_wordle_solver

lint: ## lint the app using flake8 and ruff
	@echo "📝 linting..."
	$(BIN)/flake8 app.py flask_wordle_solver
	$(BIN)/ruff app.py flask_wordle_solver

typing: ## type check the app using mypy
	@echo "📝 type checking..."
	$(BIN)/mypy app.py flask_wordle_solver
