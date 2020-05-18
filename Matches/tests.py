import json

import pika
from demjson import decode
from django.urls import reverse
from rest_framework.test import APITestCase

from Matches.management.commands.startconsumer import QUEUE_NAME, RABBITMQ_HOST, create_or_update_match
from Matches.models import Match


def send_message_to_broker(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          body=message)
    connection.close()


class MessagesProcessingTests(APITestCase):
    def test_when_message1_is_sent_application_exposes_the_correct_object(self):
        message1 = open('Matches/fixtures/message1.json', 'r').read()
        create_or_update_match(decode(message1))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': '1', 'url': 'https://www.source1.org/matches/1/',
                                     'tournament': {'id': 15, 'name': 'Overbayes Season 1'},
                                     'title': {'name': 'overcooked'},
                                     'teams': [{'id': 1, 'name': 'Bayes Esports Team 1'},
                                               {'id': 2, 'name': 'Bayes Team 2'}],
                                     'state': 1, 'bestof': '3',
                                     'scores': [{'id': 1, 'score': None, 'winner': None, 'match': '1', 'team': 1},
                                                {'id': 2, 'score': None, 'winner': None, 'match': '1', 'team': 2}],
                                     'date_start': '2020-01-07T14:30:00Z'})

    def test_when_message2_is_sent_after_message1_application_exposes_the_correct_object(self):
        message1 = open('Matches/fixtures/message1.json', 'r').read()
        create_or_update_match(decode(message1))

        message2 = open('Matches/fixtures/message2.json', 'r').read()
        create_or_update_match(decode(message2))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': '1', 'url': 'https://www.source1.org/matches/1/',
                                     'tournament': {'id': 15, 'name': 'Overbayes Season 1 - Group Stage'},
                                     'title': {'name': 'overcooked'},
                                     'teams': [{'id': 2, 'name': 'Bayes Team 2'}, {'id': 3, 'name': 'Bayes Team 3'}],
                                     'state': 2, 'bestof': '3',
                                     'scores': [{'id': 3, 'score': 2, 'winner': True, 'match': '1', 'team': 2},
                                                {'id': 4, 'score': 0, 'winner': False, 'match': '1', 'team': 3}],
                                     'date_start': '2020-01-07T15:00:00Z'})
