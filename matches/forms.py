from django import forms
from .models import Matches


class MatchesForm(forms.ModelForm):

    class Meta:
        model = Matches
        fields = ['local', 'time_casa', 'time_fora', 'placar_casa', 'placar_fora', 'tipo_competicao', 'data_partida']
        