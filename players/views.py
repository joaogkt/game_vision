from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from .forms import PlayerForm
import os
from django.contrib.auth.decorators import login_required
from player_stats.models import PlayerDesempenhoGeral



@login_required(login_url='login')
def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})


@login_required(login_url='login')
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    desempenho = PlayerDesempenhoGeral.objects.filter(jogador=player).first()
    return render(request, 'player_detail.html', {'player': player, 'desempenho': desempenho})

@login_required(login_url='login')
def player_create(request):
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

@login_required(login_url='login')
def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk)
    old_photo = player.photo.path if player.photo else None

    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_detail', pk=player.pk)
    else:
        form = PlayerForm(instance=player)

    return render(request, 'player_form.html', {'form': form})


@login_required(login_url='login')
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        player.delete()
        return redirect('player_list')
    return render(request, 'player_confirm_delete.html', {'player': player})
