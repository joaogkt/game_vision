from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import PlayerStats
from .forms import PlayerStatsForm

# Create your views here.
def player_stats_list(request):
    player_stats = PlayerStats.objects.all()
    return render(request, 'player_stats_list.html', {'players': player_stats})

def player_stats_create(request):
    if request.method == "POST":
        form = PlayerStatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_stats_list')
    else:
        form = PlayerStatsForm()
    return render(request, 'player_stats_form.html', {'form': form})


def player_stats_update(request, pk):
    player_stats = get_object_or_404(PlayerStats, pk=pk)

    if request.method == 'POST':
        form = PlayerStatsForm(request.POST, request.FILES, instance=player_stats)
        if form.is_valid():
            form.save()
            return redirect('player_stats_detail', pk=player_stats.pk)
    else:
        form = PlayerStatsForm(instance=player_stats)
    return render(request, 'player_stats_form.html', {'form': form})


def player_stats_detail(request, pk):
    player_stat = get_object_or_404(PlayerStats, pk=pk)
    return render(request, 'player_stats_detail.html', {'player_stat': player_stat})


def player_stats_delete(request, pk):
    player_stats = get_object_or_404(PlayerStats, pk=pk)
    if request.method == "POST":
        player_stats.delete()
        return redirect('player_stats_list')
    return render(request, 'player_stats_confirm_delete.html', {'player_stats': player_stats})