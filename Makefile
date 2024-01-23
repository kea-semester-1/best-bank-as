lint: ## Run linter
	@echo "Running linter..."
	poetry run isort .
	poetry run black .
	poetry run ruff --fix .
	poetry run mypy .

run: ## Run the application
	@echo "Running application..."
	docker-compose -f docker-compose.yml up --build

migration: ## Migrate to latest database version
	@echo "Upgrading database..."
	docker container exec $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py migrate

migration-revert: ## Revert to previous database version
	@echo "Downgrading database..."
	docker container exec $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py migrate best_bank_as zero

migration-generate: ## Generate a new migration file
	@echo "Generating migration file..."
	docker container exec $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py makemigrations

migration-generate-empty: ## Generate a new empty migration file
	@echo "Generating empty migration file..."
	docker container exec $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py makemigrations --empty best_bank_as


shell: ## Open a shell in the container
	@echo "Opening shell..."
	docker container exec -it $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python3 manage.py shell
	
superuser: ## Create superuser
	@echo "Creating superuser..."
	docker container exec -it $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py createsuperuser

reboot: # Remove container, images and volumes
	@echo "Removing containers"
	docker rm $$(docker ps -aq)
	@echo "Removing images"
	docker rmi $$(docker images -q)  
	@echo "Removing volumes"
	docker volume rm $$(docker volume ls -q)

provision: ## Create provisions
	@echo "Creating provision..."
	docker container exec -it $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py provision

demodata: ## Create demodata
	@echo "Creating demodata..."
	docker container exec -it $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py demodata

test: ## Run tests
	@echo "Running tests..."
	docker container exec -it $$(docker ps | grep best-bank-as_app | awk '{print $$1}') python manage.py test