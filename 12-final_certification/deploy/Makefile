DB_HOST = localhost
DB_PORT = 5432
DB_NAME = subscriptions
DB_USER = postgres
DB_PASSWORD = 1234

.PHONY: up-db
up-db:
	docker-compose -f docker-compose.yml up -d

.PHONY: init-db
init-db:
	PGPASSWORD=$(DB_PASSWORD) psql -U $(DB_USER) -d $(DB_NAME) -p $(DB_PORT) -h $(DB_HOST) -a -f init.sql

.PHONY: down-db
down-db:
	docker-compose -f docker-compose.yml down
