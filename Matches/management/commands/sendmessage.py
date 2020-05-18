import os

import pika
from django.core.management.base import BaseCommand

QUEUE_NAME = os.getenv('QUEUE_NAME', 'matches')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')


class Command(BaseCommand):
    help = 'Send message to RabbitMQ RabbitMQ'

    def add_arguments(self, parser):
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        data = open(options.get('message'), 'r').read()
        self.send_message_to_broker(data)

    @staticmethod
    def send_message_to_broker(message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(exchange='',
                              routing_key=QUEUE_NAME,
                              body=message)
        connection.close()
