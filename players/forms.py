from django import forms
from .models import Player
from gerencia.models import Turma

class PlayerForm(forms.ModelForm):

    # remove_photo = forms.BooleanField(required=False, label="Remover foto")
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'birth_date', 'nationality', 'position', 'team',
                   'responsavel', 'turma', 'status', 'photo']
        