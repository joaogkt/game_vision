from django import forms
from .models import Turma, Responsavel, Treinador


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'treinador', 'faixa_etaria', 'horario_treino', 'team']

class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['nome', 'email', 'telefone', 'data_nascimento', 'cpf']

class TreinadorForm(forms.ModelForm):
    class Meta:
        model = Treinador
        fields = ['nome', 'email', 'telefone', 'data_nascimento', 'cpf']
