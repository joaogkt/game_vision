from django import forms
from .models import PlayerStats
from django.core.exceptions import ValidationError

def validate_integer(value):
    if not isinstance(value, int):
        raise ValidationError(f"{value} não é um número inteiro válido.")

class PlayerStatsForm(forms.ModelForm):

    class Meta:
        model = PlayerStats
        fields = ['jogador', 'jogo', 'minutos_jogados',
                   'gols', 'assistencia', 'passes_certos',
                     'passes_errados', 'desarmes', 'cartao_vermelho',
                       'cartao_amarelo', 'nota']
        widgets = {
            'minutos_jogados': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'gols': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'assistencia': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'passes_certos': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'passes_errados': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'desarmes': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'cartao_vermelho': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'cartao_amarelo': forms.NumberInput(attrs={'type': 'number', 'min': 0}),
            'nota': forms.NumberInput(attrs={'type': 'number', 'min': 0, 'step': '0.1'}),
        }
        
    def clean_minutos_jogados(self):
        minutos_jogados = self.cleaned_data.get('minutos_jogados')
        if not isinstance(minutos_jogados, int):
            raise ValidationError("Minutos jogados deve ser um número inteiro.")
        return minutos_jogados

    def clean_gols(self):
        gols = self.cleaned_data.get('gols')
        if not isinstance(gols, int):
            raise ValidationError("Gols deve ser um número inteiro.")
        return gols
    
    def clean_passes_certos(self):
        passes_certos = self.cleaned_data.get('passes_certos')
        if not isinstance(passes_certos, int):
            raise ValidationError("Passes certos deve ser um número inteiro.")
        return passes_certos
    
    def clean_passes_errados(self):
            passes_errados = self.cleaned_data.get('passes_errados')
            if not isinstance(passes_errados, int):
                raise ValidationError("Passes errados deve ser um número inteiro.")
            return passes_errados
  
    def clean_desarmes(self):
            desarmes = self.cleaned_data.get('desarmes')
            if not isinstance(desarmes, int):
                raise ValidationError("Desarmes deve ser um número inteiro.")
            return desarmes

    def clean_cartao_vermelho(self):
            cartao_vermelho = self.cleaned_data.get('cartao_vermelho')
            if not isinstance(cartao_vermelho, int):
                raise ValidationError("Cartão vermelho deve ser um número inteiro.")
            return cartao_vermelho
    
    def clean_cartao_amarelo(self):
            cartao_amarelo = self.cleaned_data.get('cartao_amarelo')
            if not isinstance(cartao_amarelo, int):
                raise ValidationError("Cartão vermelho deve ser um número inteiro.")
            return cartao_amarelo