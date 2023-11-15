API_KEY ?= NOT_EXIST
API_SECRET ?= NOT_EXIST

# These targets are not files
.PHONY: help check test lint lint-fix

help: ## Display this help message
	@echo "Please use \`make <target>\` where <target> is one of"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; \
	{printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

lint:  ## Run linters
	black --check original_sdk
	flake8 --ignore=E501,W503 original_sdk
	mypy original_sdk

lint-fix:
	black original_sdk
	isort original_sdk

test:  ## Run tests
	API_KEY=$(API_KEY) API_SECRET=$(API_SECRET) pytest original_sdk/tests

check: lint test  ## Run linters + tests

reviewdog:
	black --check --diff --quiet original_sdk | reviewdog -f=diff -f.diff.strip=0 -filter-mode="diff_context" -name=black -reporter=github-pr-review
	flake8 --ignore=E501,W503 original_sdk | reviewdog -f=flake8 -name=flake8 -reporter=github-pr-review
	mypy --show-column-numbers --show-absolute-path original_sdk | reviewdog -efm="%f:%l:%c: %t%*[^:]: %m" -name=mypy -reporter=github-pr-review
