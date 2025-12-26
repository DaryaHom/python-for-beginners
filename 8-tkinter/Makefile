.PHONY: up-db
up-db:
	docker-compose -f docker-compose.yml up -d

.PHONY: init-db
init-db:
	PGPASSWORD=1234 psql -U postgres -d te1 -p 5432 -h 127.0.0.1 -a -f init.sql

.PHONY: down-db
down-db:
	docker-compose -f docker-compose.yml down -v
