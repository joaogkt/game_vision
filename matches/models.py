from django.db import models
import teams.models

# Create your models here.
class Matches(models.Model):
    local = models.CharField(max_length=50)
    time_casa = models.ForeignKey(teams.models.Team, on_delete=models.CASCADE, related_name='matches_casa')
    time_fora = models.ForeignKey(teams.models.Team, on_delete=models.CASCADE, related_name='matches_fora')
    placar_casa = models.IntegerField()
    placar_fora = models.IntegerField()
    tipo_competicao = models.CharField(max_length=200)