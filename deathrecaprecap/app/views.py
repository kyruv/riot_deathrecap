from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.riot.simple_request import DeathData
from app.riot.player_request import PlayerGames
from app.riot.champs import ChampNames

def index(request):
    return render(request, 'player.html', {'image_names': ChampNames.images})

def process_form(request):
    if request.method == 'POST':
        # Get data from the submitted form
        gameid = request.POST.get('gameid', '')
        return redirect('game', gameid=gameid)
    else:
        # Handle GET requests or other cases
        return HttpResponse("Invalid request method")

def game(request, gameid):
    death_data = DeathData().create(gameid)

    return render(request, 'index.html', {'data': death_data, 'image_names': ChampNames.images})

def process_player(request):
    if request.method == 'POST':
        # Get data from the submitted form
        playerid = request.POST.get('playerid', '')
        tag = request.POST.get('tagid', '')
        return redirect('player', playerid=playerid+"-"+tag, start=0)
    else:
        # Handle GET requests or other cases
        return HttpResponse("Invalid request method")

def player_no_start(request, playerid):
    return redirect('player', playerid=playerid, start=0)

def player(request, playerid, start):
    player_games = PlayerGames().create(playerid, start)

    return render(request, 'player.html', {'recent_games': player_games, 'image_names': ChampNames.images})


