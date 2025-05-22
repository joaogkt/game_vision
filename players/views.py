from django.shortcuts import render, get_object_or_404, redirect
from .models import Player, Faltas
from .forms import PlayerForm
import os
from django.contrib.auth.decorators import login_required
from player_stats.models import PlayerDesempenhoGeral, PlayerStats
from matches.models import Matches
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from core.views import is_admin

@login_required(login_url='login')
def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})


@login_required(login_url='login')
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    presencas = Faltas.objects.filter(aluno=player).order_by('-data')

    desempenho = PlayerDesempenhoGeral.objects.filter(jogador=player).first()
    partidas_jogadas = Matches.objects.filter(id__in=PlayerStats.objects.filter(jogador=player).values_list('jogo', flat=True))

    return render(request, 'player_detail.html', {'player': player, 'desempenho': desempenho, 'partidas': partidas_jogadas, 'presencas': presencas})

@user_passes_test(is_admin)
@login_required(login_url='login')
def player_create(request):
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print("ok")
            form.save()
            return redirect('player_list')
    else:
        print("Not ok")
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
@login_required(login_url='login')
def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    player.delete()
    messages.success(request, "Jogador excluído com sucesso!")
    return redirect('player_list') 
    # player = get_object_or_404(Player, pk=pk)
    # if request.method == "POST":
    #     player.delete()
    #     return redirect('player_list')
    # return render(request, 'player_confirm_delete.html', {'player': player})
