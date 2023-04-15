init:
	cp .env.dist .env

build:
	docker-compose up -d --build

upgrade_migrations:
	docker-compose exec api alembic upgrade head