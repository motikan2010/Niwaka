
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d

sh:
	docker compose exec app bash

ps:
	docker compose ps
