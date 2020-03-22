# cat -e -t -v Makefile
.PHONY: all say_hello build up down

all: say_hello up

say_hello:
	@echo "Hello Django"

up:
	@echo "Starting docker containers..."
	docker-compose up -d

down:
	@echo "Cleaning up docker containers..."
	docker-compose down -v

build:
	@echo "Building docker containers..."
	docker-compose build

build_no_cache:
	@echo "Building docker containers..."
	docker-compose build --no-cache

run_tests:
	@echo "Running unit tests in docker containers..."
	docker-compose run --rm web-1 sh -c "python manage.py test"

generate_secret:
	@echo "Generating secret key..."
	docker-compose run --rm web-1 sh -c "python manage.py generate_secretkey 50"

access:
	@echo "Accessing django app container..."
	docker-compose exec web-1 sh