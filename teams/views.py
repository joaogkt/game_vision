from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Team
from players.models import Player
from .forms import TeamForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from core.views import is_admin
from player_stats.models import PlayerStats, PlayerDesempenhoGeral

# Create your views here.


@login_required(login_url='login')
def team_list(request):
    teams = Team.objects.all()
    player = Player.objects.all()
    return render(request, 'team_list.html', {'teams': teams, 'players': player})


@login_required(login_url='login')
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    players = Player.objects.filter(team=team)
        
    desempenho_geral = PlayerDesempenhoGeral.objects.filter(jogador__in=players)

    top_goleador = desempenho_geral.order_by('-total_gols').first()
    top_assistencias = desempenho_geral.order_by('-total_assistencias').first()
    top_passes = desempenho_geral.order_by('-total_passes_certos').first()
    top_desarmes = desempenho_geral.order_by('-total_desarmes').first()
    melhor_avaliado = desempenho_geral.order_by('-media_nota').first()
    mais_partidas = desempenho_geral.order_by('-total_partidas').first()

    print(team, players, top_assistencias, top_desarmes, top_goleador, top_passes, melhor_avaliado)

    context = {
       'team': team,
       'players': players,
       'top_goleador': top_goleador,
       'top_assistencias': top_assistencias,
       'top_passes': top_passes,
       'top_desarmes': top_desarmes,
       'melhor_avaliado': melhor_avaliado,
        'mais_partidas': mais_partidas
        }

    return render(request, 'team_detail.html', context)

@user_passes_test(is_admin)
@login_required(login_url='login')
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'team_form.html', {'form': form})

@user_passes_test(is_admin)
@login_required(login_url='login')
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm(instance=team)
    return render(request, 'team_form.html', {'form': form})



@user_passes_test(is_admin)
@login_required(login_url='login')
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    messages.success(request, "Jogador excluído com sucesso!")
    return redirect('team_list')

