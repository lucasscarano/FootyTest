from django.db import models

# Create your models here.

class Club(models.Model):
    club_id = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=120, null=False)
    fm_id = models.IntegerField(null=True)

    def __str__(self):
        return self.club_name

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=120, null=False)
    fm_id = models.IntegerField(null=True)
    nationality = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.player_name

class PlayerClubs(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
