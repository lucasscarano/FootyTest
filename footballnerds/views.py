import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from unidecode import unidecode

from footballnerds.forms import RegistrationForm
from footballnerds.models import Player, Game, User, GamePlayer


def index(request):
    return render(request, "index.html")

# TODO: Change style
def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])

            if user:
                login(request, user)
                return redirect('start_game')
            else:
                # Log error if user is not authenticated
                form.add_error(None, "Authentication failed. Please try again.")
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {
        'form': form,
    })

# TODO: Add error messages
# TODO: Change style
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('start_game')
        else:
            return redirect('login')
    else:
        return render(request, "login.html")


def play_as_guest(request):
    count = User.objects.filter(username__startswith="Guest").count()
    username = f"Guest #{count + 1}"
    password = "ajhdfkjhkajdshf" # TODO: Set random password

    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    login(request, user)
    return redirect("start_game")

def start_game(request):
    user = request.user

    # TEMPORAL
    user2, _ = User.objects.get_or_create(
        username="Felipe",
        nationality_id=9,
    )

    new_game = Game.objects.create(
        user1=user,
        user2=user2,
        user_turn=user
    )

    # Maybe it's better to pass the game_id as a parameter to every
    # function and not search it in session every time I want to modify whose turn it is
    request.session["game_id"] = new_game.game_id

    first_player = get_random_player(request)

    request.session["played_players"] = [first_player.player_id]

    return render(request, "start_game.html",
                  {'first_player': first_player,
                   "user1": user,
                   "user2": user2,
                   "game_turn": new_game.turn_number,})

def get_random_player(request):
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
        players_objs = Player.objects.all().order_by('-max_transfer_value')

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
        game_id = request.session.get("game_id")
        game = Game.objects.get(game_id=game_id)
        load_game_player(game, new_player)
        game.switch_turn()
        request.session["last_player_id"] = new_player.player_id
        request.session["played_players"].append(new_player.player_id)
        return JsonResponse({'status': 200, 'player':{
                        "player_id": new_player.player_id,
                        "player_name": new_player.player_name,
                        "max_transfer_value":new_player.max_transfer_value,
                        "flag_url":new_player.nationality.flag_url,
                        "clubs": common_clubs,
                        "player_photo_url": new_player.player_photo_url,
                        },
                             "game_turn": game.turn_number})

    return JsonResponse({'status': 400, 'message': "There's no clubs in common between the players."})

def load_game_player(game, player):
    GamePlayer.objects.create(game=game, player=player,
                              added_by=game.user_turn,
                              turn_number=game.turn_number)

@csrf_exempt
def end_game(request):
    game_id = request.session.get("game_id")
    game = Game.objects.get(game_id=game_id)

    user_lost = game.user_turn
    user_won = game.user2 if user_lost == game.user1 else game.user1

    user_lost.lose()
    user_won.win()

    game.is_active = False
    game.save()
    user_lost.save()
    user_won.save()

    request.session.pop("game_id")
    request.session.pop("played_players")
    request.session.pop("last_player_id")

    return JsonResponse({'status': 200})



# TODO: Limit on played clubs links? I.E. Liverpool has been played X times already
# TODO: Limited skips? Go back to the other user with the same player. OR play a random top player (>40m tm)
# TODO: Keep user logged in.
# TODO: Accelerate timer as turns go on. Maybe after turn 20, 15s max or something.
