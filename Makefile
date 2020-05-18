DOCKER_TAG ?= $(shell git rev-parse HEAD)
DOCKER_IMAGE = esportsapi:$(DOCKER_TAG)
DB_PASSWORD ?= postgres
DB_USER ?= postgres

.PHONY:
build:
	DOCKER_IMAGE=$(DOCKER_IMAGE) DB_PASSWORD=$(DB_PASSWORD) DB_USER=$(DB_USER) docker-compose build

.PHONY:
test: build
	docker run --rm -e DB_PASSWORD=$(DB_PASSWORD) -e DB_USER=$(DB_USER) -it $(DOCKER_IMAGE)  python manage.py test

.PHONY:
run: build
	DOCKER_IMAGE=$(DOCKER_IMAGE) DB_PASSWORD=$(DB_PASSWORD) DB_USER=$(DB_USER) docker-compose up -d

.PHONY:
stop:
	DOCKER_IMAGE=$(DOCKER_IMAGE) DB_PASSWORD=$(DB_PASSWORD) DB_USER=$(DB_USER) docker-compose down


.PHONY:
migrate:
	DOCKER_IMAGE=$(DOCKER_IMAGE) USE_POSTGRES=true DB_PASSWORD=$(DB_PASSWORD) DB_USER=$(DB_USER) docker-compose run worker python manage.py migrate

.PHONY:
push_messages:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message1.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message2.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message3.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message4.json
