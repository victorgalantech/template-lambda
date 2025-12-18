.PHONY: help install test lint format clean docker-build docker-run terraform-init terraform-plan terraform-apply

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies with Poetry
	poetry install

run-local: ## Run Lambda function locally with example data
	poetry run python entrypoint.py

test: ## Run unit tests with coverage
	poetry run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

test-verbose: ## Run unit tests with verbose output
	poetry run pytest tests/ -v --cov=src --cov-report=term-missing

lint: ## Run linting checks
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/
	poetry run flake8 src/ tests/
	poetry run mypy src/

format: ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf dist
	rm -rf build

docker-build: ## Build Docker image
	docker build -t lambda-function:latest .

docker-run: ## Run Docker container locally
	docker run -p 9000:8080 lambda-function:latest

docker-test: ## Test Docker container locally
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
		-d '{"body": "{\"name\": \"Docker Test\"}"}'

terraform-init: ## Initialize Terraform
	cd terraform && terraform init

terraform-plan: ## Run Terraform plan
	cd terraform && terraform plan

terraform-apply: ## Apply Terraform changes
	cd terraform && terraform apply

terraform-destroy: ## Destroy Terraform resources
	cd terraform && terraform destroy

terraform-fmt: ## Format Terraform files
	cd terraform && terraform fmt -recursive

terraform-validate: ## Validate Terraform configuration
	cd terraform && terraform validate

all: install lint test ## Run install, lint, and test
