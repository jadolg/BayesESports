DOCKER_TAG ?= $(shell git rev-parse HEAD)
DOCKER_IMAGE = esportsapi:$(DOCKER_TAG)

.PHONY:
build:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose build

.PHONY:
test: build
	docker run --rm -it $(DOCKER_IMAGE) python manage.py test

.PHONY:
run:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose up

.PHONY:
push_messages:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message1.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message2.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message3.json
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker-compose run worker python manage.py sendmessage Matches/fixtures/message4.json
