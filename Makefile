make lint: ## Run linter
	@echo "Running linter..."
	poetry run isort .
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

