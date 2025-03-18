from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Club(models.Model):
    club_id = models.IntegerField(primary_key=True)
    club_name = models.CharField(max_length=120, null=False)
    logo_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.club_name

class Player(models.Model):
    player_id = models.IntegerField(primary_key=True)
    player_name = models.CharField(max_length=120, null=False)
    nationality = models.ForeignKey('Nationality', on_delete=models.CASCADE)
    max_transfer_value = models.CharField(max_length=20, null=True)
    player_photo_url = models.CharField(max_length=200, null=True)
    # TODO: popularity? how often a player is played?

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


class Nationality(models.Model):
    nationality_id = models.IntegerField(primary_key=True)
    nationality_name = models.CharField(max_length=120, null=False)
    flag_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nationality_name

# TODO: Change for AbstractUser
class User(models.Model):
    username = models.CharField(max_length=120, null=False, unique=True)
    nationality = models.ForeignKey('Nationality', on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def lose(self):
        self.losses +=1
        self.save()

    def win(self):
        self.wins +=1
        self.save()

    def record(self):
        return str(self.wins) + ' - ' + str(self.losses)

class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user2')
    turn_number = models.IntegerField(default=1)
    user_turn = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_turn')
    is_active = models.BooleanField(default=True)

    def switch_turn(self):
        self.user_turn = self.user1 if self.user_turn == self.user2 else self.user2
        self.turn_number += 1
        self.save()


# To get statistics on players played in each game
class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="played_players")
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    added_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    turn_number = models.IntegerField(default=1)
