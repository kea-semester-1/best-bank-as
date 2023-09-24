make lint: ## Run linter
	@echo "Running linter..."
	poetry run isort .
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

make run: ## Run the application
	@echo "Running application..."
	docker-compose -f docker-compose.yml up --build