from django import forms
from .models import PlayerStats


class MatchesForm(forms.ModelForm):

    class Meta:
        model = PlayerStats
        fields = ['jogador', 'jogo', 'minutos_jogados',
                   'gols', 'assistencia', 'passes_certos',
                     'passes_errados', 'desarmes', 'cartao_vermelho',
                       'cartao_amarelo', 'nota']
        