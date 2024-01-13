from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('process_form/', views.process_form, name='process_form'),
    path('process_player/', views.process_player, name='process_player'),
    path('game/<str:gameid>/', views.game, name='game'),
    path('player/<str:playerid>/', views.player_no_start, name='player'),
    path('player/<str:playerid>/<int:start>/', views.player, name='player'),
]