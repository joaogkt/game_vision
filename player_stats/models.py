from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from players.models import Player
from matches.models import Matches

class PlayerStats(models.Model):
    jogador = models.ForeignKey(Player, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Matches, on_delete=models.CASCADE)
    minutos_jogados = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    gols = models.IntegerField(default=0)
    assistencia = models.IntegerField(default=0)
    passes_certos = models.IntegerField(default=0)
    passes_errados = models.IntegerField(default=0)
    desarmes = models.IntegerField(default=0)
    cartao_vermelho = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], default=0)
    cartao_amarelo = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], default=0)
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0.0)

    def __str__(self):
        return f"{self.jogador} - {self.jogo}"
