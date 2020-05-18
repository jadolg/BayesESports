from django.db import models


class Match(models.Model):
    id = models.CharField(primary_key=True, max_length=250)
    url = models.CharField(max_length=250)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='matches', null=True)
    title = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='matches', null=True)
    teams = models.ManyToManyField('Team', related_name='matches')
    state = models.IntegerField(null=True)
    bestof = models.CharField(max_length=250, null=True)
    date_start = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "matches"

    def __str__(self):
        return f'{self.id}'


class Tournament(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.id} {self.name}'


class Title(models.Model):
    name = models.CharField(primary_key=True, max_length=250)

    def __str__(self):
        return f'{self.name}'


class Team(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class Score(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE, related_name='scores')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(null=True, default=None)
    winner = models.BooleanField(null=True, default=None)

    def __str__(self):
        return f'{self.match} {self.team} {self.score} {self.winner}'
