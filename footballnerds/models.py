from django.db import models

# Create your models here.

class Team(models.Model):
    team_id = models.CharField(primary_key=True, max_length=10)
    team_name = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.team_name

class Player(models.Model):
    player_id = models.CharField(primary_key=True, max_length=10)
    player_name = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.player_name

class PlayerTeams(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
