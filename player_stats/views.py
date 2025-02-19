from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import PlayerStats
from .forms import PlayerStatsForm
from django.contrib.auth.decorators import login_required
from players.models import Player
from .models import PlayerDesempenhoGeral
from django.db.models import Sum, Count, F
# Create your views here.

@login_required(login_url='login')
def player_stats_list(request):
    player_stats = PlayerStats.objects.all()
    return render(request, 'player_stats_list.html', {'players': player_stats})




@login_required(login_url='login')
def player_stats_create(request):
    if request.method == "POST":
        form = PlayerStatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_stats_list')
    else:
        form = PlayerStatsForm()
    return render(request, 'player_stats_form.html', {'form': form})


@login_required(login_url='login')
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


@login_required(login_url='login')
def player_stats_detail(request, pk):
    player_stat = get_object_or_404(PlayerStats, pk=pk)
    return render(request, 'player_stats_detail.html', {'player_stat': player_stat})


@login_required(login_url='login')
def player_stats_delete(request, pk):
    player_stats = get_object_or_404(PlayerStats, pk=pk)
    if request.method == "POST":
        player_stats.delete()
        return redirect('player_stats_list')
    return render(request, 'player_stats_confirm_delete.html', {'player_stats': player_stats})

@login_required(login_url='login')
def desempenho_geral(request):
    jogadores = Player.objects.all()
    desempenho_total = []

    for jogador in jogadores:
        stats = PlayerStats.objects.filter(jogador=jogador).aggregate(
            total_gols=Sum('gols', default=0),
            total_assistencias=Sum('assistencia', default=0),
            total_passes_certos=Sum('passes_certos', default=0),
            total_passes_errados=Sum('passes_errados', default=0),
            total_desarmes=Sum('desarmes', default=0),
            total_cartoes_vermelhos=Sum('cartao_vermelho', default=0),
            total_cartoes_amarelos=Sum('cartao_amarelo', default=0),
            total_partidas=Count('id') 
        )

        if stats['total_partidas'] > 0: 
            media_nota = (
                PlayerStats.objects.filter(jogador=jogador).aggregate(Sum('nota'))['nota__sum'] or 0
            ) / max(stats['total_partidas'], 1) 

            desempenho, created = PlayerDesempenhoGeral.objects.update_or_create(
                jogador=jogador,
                defaults={
                    'total_gols': stats['total_gols'],
                    'total_assistencias': stats['total_assistencias'],
                    'total_passes_certos': stats['total_passes_certos'],
                    'total_passes_errados': stats['total_passes_errados'],
                    'total_desarmes': stats['total_desarmes'],
                    'total_cartoes_vermelhos': stats['total_cartoes_vermelhos'],
                    'total_cartoes_amarelos': stats['total_cartoes_amarelos'],
                    'media_nota': media_nota,
                    'total_partidas': stats['total_partidas'], 
                }
            )

            desempenho_total.append(desempenho) 

    return render(request, 'player_stats_total.html', {'desempenho_total': desempenho_total})

def desempenho_graficos(request):
    return render(request, 'player_stats_graficos.html')