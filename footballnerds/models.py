from django.db import models

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


class User(models.Model):
    username = models.CharField(max_length=120, null=False)
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
        return self.wins, ' - ', self.losses

class Game(models.Model):
    user1 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user2')
    current_turn = models.IntegerField(default=0)
    user_turn = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_turn')

    def switch_turn(self):
        self.user_turn = self.user1 if self.user_turn == self.user2 else self.user2
        self.current_turn += 1
        self.save()