build:
	@docker-compose build --no-cache

bash:
	@docker-compose run --rm api bash

run:
	@docker-compose up

test:
	@docker-compose run --rm api pytest

down:
	@docker-compose down -v
