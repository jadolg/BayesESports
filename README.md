# Bayes eSports coding exercise

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/manual/html_node/index.html)

## How to test

Executing `make test` will execute all the tests inside a docker container.

## How to run

Executing `make run` will start:

1. Postgres database
2. RabbitMQ
3. Web service exposing the matches under `/v1`
4. Consumer service that gets the data from RabbitMQ

To push the messages to the queue execute `make push_messages`. It will use a Django management command to connect to RabbitMQ using pika and send the desired message.

## How it works

### Web service

Since the only purpose of the service is serving the data already stored I decided to use the simplest possible solution which would be Django REST Framework, since it comes packed with tools like the ModelSerializer that behaves very good for the more standard cases. On top of that, DRF supports django-filter, so filtering by any of the fields becomes an easy, already tested task. The web service is exposing the API under the `v1` endpoint and it's serving matches and their children.

### Consumer

Consumer is also inside the Django application, but it's packed as a manage command. This way you can use the same codebase and all the Django goodies (ORM and existing configuration) to manage the received data. Since the application will be running on a container that restarts always, I decided to let errors happen as it's usually better for logging purposes and just allow the mechanism to try to reconnect if RabbitMQ dies or misbehaves. This way, in my opinion, you have a better idea of what's happening with the application all the time.
Consumer will use pika to pull the messages from the RabbitMQ server and will persist the data on the Database to be immediately served by Django.  
