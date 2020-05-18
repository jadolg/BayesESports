from django.contrib import admin

from Matches.models import Match, Tournament, Team, Score, Title

admin.site.register(Match)
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Score)
admin.site.register(Title)
