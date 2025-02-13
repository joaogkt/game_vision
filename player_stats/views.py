from django.shortcuts import render, HttpResponse
from .models import PlayerStats

# Create your views here.
def player_stats_list(request):
    player_stats = PlayerStats.objects.all()
    return render(request, 'player_stats_list.html', {'players': player_stats})