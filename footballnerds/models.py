from django.db import models

# Create your models here.

class Club(models.Model):
    club_id = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=120, null=False)
    fm_id = models.IntegerField(null=True)
    # TODO: club_logo

    def __str__(self):
        return self.club_name

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=120, null=False)
    fm_id = models.IntegerField(null=True)
    nationality = models.CharField(max_length=120, null=True)
    # TODO: player_photo
    # TODO: popularity? could be related to how much a player is played or max-transfer-value

    def __str__(self):
        return self.player_name

    @property
    def clubs(self):
        clubs = []
        player_clubs = PlayerClubs.objects.filter(player_id=self.player_id)
        for player_club in player_clubs:
            clubs.append(Club.objects.filter(club_id=player_club.club_id))

        return clubs

class PlayerClubs(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

# TODO: Player1 and Player2 classes
