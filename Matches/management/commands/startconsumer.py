import logging
import os

from demjson import decode
import pika
from dateutil import parser
from django.core.management.base import BaseCommand

from Matches.models import Tournament, Title, Team, Match, Score

QUEUE_NAME = os.getenv('QUEUE_NAME', 'matches')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')


class Command(BaseCommand):
    help = 'Start receiving messages from RabbitMQ'

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)

        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_consume(QUEUE_NAME, self.on_message)
        logging.info('start consuming')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()

    @staticmethod
    def on_message(channel, method_frame, header_frame, body):
        try:
            logging.info(f'got message {method_frame.delivery_tag}')
            data = decode(body)  # contrary to the default json library, demjson can deal with malformed json
            create_or_update_match(data)
        finally:
            logging.info(f'ack message {method_frame.delivery_tag}')
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def create_or_update_match(data):
    source = data.get('source')

    tournament_data = data.get('data').get('tournament')
    tournament = create_or_update_tournament(source, tournament_data)

    title_data = data.get('data').get('title')
    title = Title.objects.get_or_create(name=title_data.lower().strip())[0]
    title.save()

    teams_data = data.get('data').get('teams')
    teams = create_or_update_teams(teams_data)

    match = Match.objects.get_or_create(id=data.get('data').get('id'))[0]
    match.tournament = tournament
    match.title = title
    match.teams.set(teams)
    match.url = data.get('data').get('url')
    match.state = data.get('data').get('state')
    match.bestof = data.get('data').get('bestof')
    match.date_start = parser.parse(data.get('data').get('date_start_text'))
    match.scores.all().delete()
    match.save()

    scores_data = data.get('data').get('scores')

    for score_data in scores_data:
        team = Team.objects.get(id=score_data.get('team'))
        score = Score.objects.get_or_create(match=match, team=team)[0]
        score.score = score_data.get('score')
        score.winner = score_data.get('winner')
        score.save()


def create_or_update_teams(teams_data):
    teams = []
    for team_data in teams_data:
        team = Team.objects.get_or_create(id=team_data.get('id'))[0]
        team.name = team_data.get('name')
        team.save()
        teams.append(team)
    return teams


def create_or_update_tournament(source, tournament_data):
    if source == 'source1':
        tournament = Tournament.objects.get_or_create(id=tournament_data.get('id'))[0]
        tournament.name = tournament_data.get('name')
    elif source == 'source2' or source == 'source3':
        tournament = Tournament.objects.get_or_create(name=tournament_data)[0]
    else:
        logging.error('unknow source')
        return None

    tournament.save()
    return tournament
