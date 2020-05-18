from rest_framework import viewsets

from Matches.models import Match
from Matches.serializers import MatchSerializer
from django_filters import rest_framework as filters


class MatchFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title__name")
    tournament = filters.CharFilter(field_name="tournament__name")
    date_start_gte = filters.DateFilter(field_name="date_start", lookup_expr='gte')
    date_start_lte = filters.DateFilter(field_name="date_start", lookup_expr='lte')

    class Meta:
        model = Match
        fields = ['title', 'tournament', 'state', 'date_start_gte', 'date_start_lte']


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filterset_class = MatchFilter
