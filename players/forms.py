from django import forms
from .models import Player
from gerencia.models import Turma

class PlayerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'team' in self.data:
            try:
                team_id = int(self.data.get('team'))
                self.fields['turma'].queryset = Turma.objects.filter(team_id=team_id)
            except (ValueError, TypeError):
                self.fields['turma'].queryset = Turma.objects.none()
        elif self.instance.pk and self.instance.team:
            self.fields['turma'].queryset = Turma.objects.filter(team=self.instance.team)
        else:
            self.fields['turma'].queryset = Turma.objects.none()
    # remove_photo = forms.BooleanField(required=False, label="Remover foto")
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'birth_date', 'nationality', 'position', 'team',
                   'responsavel', 'turma', 'status', 'photo']
        