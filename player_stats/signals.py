from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import PlayerStats, PlayerDesempenhoGeral
from django.db.models import Sum

@receiver(post_delete, sender=PlayerStats)
def atualizar_desempenho_geral_apos_deletar_estatistica(sender, instance, **kwargs):
    print("Signal post_delete disparado para PlayerStats")
    jogador = instance.jogador
    try:
        desempenho = PlayerDesempenhoGeral.objects.get(jogador=jogador)
    except PlayerDesempenhoGeral.DoesNotExist:
        print("Desempenho geral não encontrado")
        return

    print(f"Atualizando desempenho para jogador {jogador}")
    desempenho.total_partidas -= 1
    desempenho.total_gols -= instance.gols
    desempenho.total_assistencias -= instance.assistencia
    desempenho.total_passes_certos -= instance.passes_certos
    desempenho.total_passes_errados -= instance.passes_errados
    desempenho.total_desarmes -= instance.desarmes
    desempenho.total_cartoes_vermelhos -= instance.cartao_vermelho
    desempenho.total_cartoes_amarelos -= instance.cartao_amarelo

    # Calculando a média das notas
    remaining_notes = PlayerStats.objects.filter(jogador=jogador).aggregate(total=Sum('nota'))['total'] or 0
    total_partidas = PlayerStats.objects.filter(jogador=jogador).count()

    if total_partidas > 0:
        desempenho.media_nota = remaining_notes / total_partidas
    else:
        desempenho.media_nota = 0.0

    if (desempenho.total_partidas <= 0 and
        desempenho.total_gols <= 0 and
        desempenho.total_assistencias <= 0 and
        desempenho.total_passes_certos <= 0 and
        desempenho.total_passes_errados <= 0 and
        desempenho.total_desarmes <= 0 and
        desempenho.total_cartoes_vermelhos <= 0 and
        desempenho.total_cartoes_amarelos <= 0):
        
        print(f"Excluindo desempenho geral do jogador {jogador} porque todas as estatísticas estão zeradas ou menores que 0")
        desempenho.delete()
    else:
        desempenho.save()
