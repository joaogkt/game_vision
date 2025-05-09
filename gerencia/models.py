from django.db import models
from teams.models import Team

# Create your models here.
class Responsavel(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome

class Treinador(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    CATEGORIA_CHOICES = [
        ('SUB-7', 'Sub-7'),
        ('SUB-9', 'Sub-9'),
        ('SUB-11', 'Sub-11'),
        ('SUB-13', 'Sub-13'),
        ('SUB-15', 'Sub-15'),
        ('SUB-17', 'Sub-17'),
        ('LIVRE', 'Livre'),
    ]
    nome = models.CharField(max_length=50)
    treinador = models.ForeignKey(Treinador, on_delete=models.CASCADE, related_name='turmas')
    faixa_etaria = models.CharField(max_length=50)
    horario_treino = models.CharField(max_length=50)
    categoria = models.CharField(choices=CATEGORIA_CHOICES, max_length=10, default='LIVRE')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Escola")

    def __str__(self):
        return self.nome