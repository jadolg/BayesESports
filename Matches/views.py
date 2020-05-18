from rest_framework import viewsets

from Matches.models import Match
from Matches.serializers import MatchSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

