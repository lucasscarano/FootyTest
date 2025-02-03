import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from footballnerds.models import Player, Club, PlayerClubs


# Create your views here.
def index(request):
    return render(request, "index.html")


# search/?players=
def search_player(request):
    players = request.GET.get("players")
    payload = []
    if players:
        players_objs = Player.objects.filter(player_name__icontains=players)

        for player in players_objs:
            payload.append(player.__str__())

    return JsonResponse({'status': 200, 'data':payload})


def validate_club(request):
    data = json.loads(request.body)
    player_name = data.get('playerName')

    #last_player_id = request.session.get("last_player_id")
    #last_player = Player.objects.filter(player_id=last_player_id)

    new_player = Player.objects.filter(player_name=player_name).first()

    if new_player:
        return JsonResponse({'status': 200, 'player':{
                        "id": new_player.player_id, #Acá podría ir la foto derecho
                        "name": new_player.player_name
                    }})

    return JsonResponse({'status': 400, })