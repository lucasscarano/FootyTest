from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_player, name="search_player"),
    path("validate-club/", views.validate_club, name="validate_club"),
    path("start-game/", views.start_game, name="start_game"),
    path("end-game/", views.end_game, name="end_game"),

]