from players.models import Player, Faltas
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Faltas)
def atualizar_total_faltas_ao_salvar(sender, instance, **kwargs):
    jogador = instance.aluno
    print("Atualizando total de faltas para o jogador:", jogador.first_name, jogador.last_name)
    # Atualiza o total de faltas do jogador
    jogador.total_faltas = jogador.faltas.filter(falta=True).count()
    print("Total de faltas atualizado:", jogador.total_faltas)
    jogador.save()