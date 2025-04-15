from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import PlayerStats
from .forms import PlayerStatsForm
from .models import Matches
from django.contrib.auth.decorators import login_required
from players.models import Player
from .models import PlayerDesempenhoGeral
from django.db.models import Sum, Count, F
import matplotlib.pyplot as plt
import io
import urllib, base64
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from core.views import is_admin
import json
# Create your views here.
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='login')
def player_stats_list(request):
    player_stats = PlayerStats.objects.all()


    return render(request, 'player_stats_list.html', {
        'players': player_stats
    })


@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
@login_required(login_url='login')
def player_stats_delete(request, pk):
    player_stats = get_object_or_404(PlayerStats, pk=pk)
    player_stats.delete()
    return redirect('player_stats_list')
    

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
        total_partidas = PlayerStats.objects.filter(jogador=jogador).values('jogo').distinct().count()

        if total_partidas > 0: 
            media_nota = (
                PlayerStats.objects.filter(jogador=jogador).aggregate(Sum('nota'))['nota__sum'] or 0
            ) / max(total_partidas, 1)
            media_nota = "{:.2f}".format(media_nota)
            
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
                    'total_partidas': total_partidas, 
                }
            )    
            desempenho_total.append(desempenho)

    return render(request, 'player_stats_total.html', {'desempenho_total': desempenho_total})

    

@login_required(login_url='login')
def desempenho_graficos(request):
    raise Exception("Entrou na view!")



@login_required(login_url='login')
def player_stats_detail(request, pk):
    player_stat = get_object_or_404(PlayerStats, pk=pk)
    player = Player.objects.all()

    labels = ['Gols', 'Assistências', 'Passes Certos', 'Passes Errados', 'Desarmes']
    values = [player_stat.gols, player_stat.assistencia, player_stat.passes_certos,
              player_stat.passes_errados, player_stat.desarmes]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'green', 'orange', 'red', 'purple'])
    plt.ylabel("Quantidade")
    plt.title(f"Desempenho na Partida - {player_stat.jogador}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode("utf-8")
    uri = f"data:image/png;base64,{string}"

    return render(request, 'player_stats_detail.html', {'player_stat': player_stat, 'player': player, 'chart': uri})


@login_required(login_url='login')
def desempenho_graficos(request):
    jogadores = Player.objects.all()
    estatisticas_jogadores = {}
    
    # Nomes dos jogadores para usar como labels
    nomes_jogadores = []
    # Arrays para diferentes estatísticas
    gols = []
    assistencias = []
    notas = []
    desarmes = []
    # Adicione outras estatísticas conforme necessário
    
    for jogador in jogadores:
        stats = PlayerDesempenhoGeral.objects.filter(jogador=jogador).first()
        
        if stats:
            nome_completo = f'{jogador.first_name} {jogador.last_name}'
            nomes_jogadores.append(nome_completo)
            gols.append(stats.total_gols)
            assistencias.append(stats.total_assistencias)
            notas.append(stats.media_nota)
            desarmes.append(stats.total_desarmes)
            
            # Também mantenha o dicionário original se necessário
            estatisticas_jogadores[nome_completo] = {
                "gols": stats.total_gols,
                "assistencias": stats.total_assistencias,
                "passes_certos": stats.total_passes_certos,
                "passes_errados": stats.total_passes_errados,
                "desarmes": stats.total_desarmes,
                "cartoes_vermelhos": stats.total_cartoes_vermelhos,
                "cartoes_amarelos": stats.total_cartoes_amarelos,
                "notas": stats.media_nota,
                "partidas": stats.total_partidas
            }
    
    return render(request, 'player_stats_graficos.html', {
        'estatisticas_jogadores': estatisticas_jogadores,
        'nomes_jogadores': json.dumps(nomes_jogadores),
        'gols': json.dumps(gols),
        'assistencias': json.dumps(assistencias),
        'notas': json.dumps(notas),
        'desarmes': json.dumps(desarmes)
    })

@login_required(login_url='login')
def comparar_jogadores(request, pk1, pk2):
    jogador1 = Player.objects.get(pk=pk1)
    jogador2 = Player.objects.get(pk=pk2)

    jogador1_stats = PlayerDesempenhoGeral.objects.filter(jogador=jogador1).first()
    jogador2_stats = PlayerDesempenhoGeral.objects.filter(jogador=jogador2).first()
    #Gols
    try:
        media_gols_jogador1 = jogador1_stats.total_gols / max(jogador1_stats.total_partidas, 1)
    except:
        media_gols_jogador1 = ''

    try:
        media_gols_jogador2 = jogador2_stats.total_gols / max(jogador2_stats.total_partidas, 1)
    except:
        media_gols_jogador2 = ""
    #Assistencias
    try:
        media_assistencias_jogador1 = jogador1_stats.total_assistencias / max(jogador1_stats.total_partidas, 1)
    except:
        media_assistencias_jogador1 = ''

    try:
        media_assistencias_jogador2 = jogador2_stats.total_assistencias / max(jogador2_stats.total_partidas, 1)
    except:
        media_assistencias_jogador2 = ""

    context = {
        'media_gols_jogador1': "{:.2f}".format(media_gols_jogador1),
        'media_gols_jogador2': "{:.2f}".format(media_gols_jogador2),
        'media_assistencias_jogador1': "{:.2f}".format(media_assistencias_jogador1),
        'media_assistencias_jogador2': "{:.2f}".format(media_assistencias_jogador2), 

    }

    return render(request, 'comparar_jogadores.html', {'jogador1': jogador1, 'jogador2': jogador2, 'jogador1_stats': jogador1_stats, 'jogador2_stats': jogador2_stats, 'context': context})

@login_required(login_url='login')
def desempenho_gols_grafico(request, pk):
    jogador = get_object_or_404(Player, id=pk)
    stats = PlayerStats.objects.filter(jogador=jogador).order_by('jogo__data')

    if not stats.exists():
        return HttpResponse("Nenhuma estatística disponível para este jogador.", status=404)

    datas = [stat.jogo.data.strftime('%d/%m/%Y') for stat in stats]
    gols = [stat.gols for stat in stats]

    plt.figure(figsize=(10, 5))
    plt.plot(datas, gols, marker='o', linestyle='-', color='b', label="Gols por jogo")
    plt.xlabel("Data da Partida")
    plt.ylabel("Gols Marcados")
    plt.title(f"Desempenho de {jogador.first_name} {jogador.last_name}")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode("utf-8")
    uri = f"data:image/png;base64,{string}"

    return render(request, 'player_stats_gols.html', {'jogador': jogador, 'chart': uri})
