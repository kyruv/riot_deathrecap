from django.http import HttpResponse
from django.shortcuts import render
from app.riot.request import DeathData
from app.riot.champs import ChampNames

def index(request):
    return render(request, 'index.html', {'image_names': ChampNames.images})

def process_form(request):
    if request.method == 'POST':
        # Get data from the submitted form
        gameid = request.POST.get('gameid', '')

        death_data = DeathData().create(gameid)

        return render(request, 'index.html', {'data': death_data, 'image_names': ChampNames.images})
    else:
        # Handle GET requests or other cases
        return HttpResponse("Invalid request method")
