from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search_player, name="search_player"),
    path("validate_club/", views.validate_club, name="validate_club"),

]