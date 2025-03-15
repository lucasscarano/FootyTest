import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from unidecode import unidecode

from footballnerds.models import Player


# Create your views here.
def index(request):
    request.session.clear()
    first_player = get_random_player(request)
    request.session["played_players"] = [first_player.player_id]

    return render(request, "index.html", {'first_player': first_player})


def get_random_player(request):
    last_player_id = request.session.get("last_player_id")

    request.session.clear()

    if last_player_id:
        random_player = Player.objects.get(player_id=last_player_id)
    else:
        random_player = Player.objects.order_by('?')
        random_player = random_player.filter(max_transfer_value__gte=40_000_000).first()

    request.session["last_player_id"] = random_player.player_id

    return random_player



# search/?players=
def search_player(request):
    players = request.GET.get("players", "").strip()
    payload = []

    if players:
        normalized_query = unidecode(players.lower())
        players_objs = Player.objects.all().order_by('max_transfer_value')

        for player in players_objs:
            if normalized_query in unidecode(player.player_name.lower()):
                payload.append(player.__str__())

    return JsonResponse({'status': 200, 'data':payload})

@csrf_exempt
def validate_club(request):
    data = json.loads(request.body)
    player_name = data.get('playerName')

    last_player_id = request.session.get("last_player_id")
    last_player = Player.objects.get(player_id=last_player_id)
    last_player_clubs = last_player.clubs

    new_player = Player.objects.filter(player_name=player_name).first()
    if new_player.player_id in request.session["played_players"]:
        return JsonResponse({'status': 400, 'message': "Player has already been played"})
    new_player_clubs = new_player.clubs

    common_clubs = []
    for x in new_player_clubs:
        for y in last_player_clubs:
            if set(x) == set(y):
                for club in x:
                    common_clubs.append([club.club_name, club.logo_url])

    if common_clubs:
        request.session["last_player_id"] = new_player.player_id
        request.session["played_players"].append(new_player.player_id)
        return JsonResponse({'status': 200, 'player':{
                        "player_id": new_player.player_id,
                        "player_name": new_player.player_name,
                        "max_transfer_value":new_player.max_transfer_value,
                        "flag_url":new_player.nationality.flag_url,
                        "clubs": common_clubs,
                        "player_photo_url": new_player.player_photo_url,
                    }})

    return JsonResponse({'status': 400, 'message': "There's no clubs in common between the players."})

# TODO: Limit on played clubs links? I.E. Liverpool has been played X times already
# TODO: Limited skips? Go back to the other user with the same player. OR play a random top player (>40m tm)
# TODO: Add number of turn being played.
