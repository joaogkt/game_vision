from django.db import models
from teams.models import Team

# Create your models here.
class Matches(models.Model):
    local = models.CharField(max_length=50)
    time_casa = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_casa')
    time_fora = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_fora')
    placar_casa = models.IntegerField()
    placar_fora = models.IntegerField()
    data_partida = models.DateField(null=True, blank=True)
    tipo_competicao = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.time_casa} {self.placar_casa} x {self.placar_fora} {self.time_fora}"