from rest_framework import serializers

from Matches.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'url', 'tournament', 'title', 'teams', 'state', 'bestof', 'scores', 'date_start']
        depth = 1
