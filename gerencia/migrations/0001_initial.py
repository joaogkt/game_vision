# Generated by Django 5.1.6 on 2025-05-09 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0002_alter_team_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treinador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('faixa_etaria', models.CharField(max_length=50)),
                ('horario_treino', models.CharField(max_length=50)),
                ('categoria', models.CharField(choices=[('SUB-7', 'Sub-7'), ('SUB-9', 'Sub-9'), ('SUB-11', 'Sub-11'), ('SUB-13', 'Sub-13'), ('SUB-15', 'Sub-15'), ('SUB-17', 'Sub-17'), ('LIVRE', 'Livre')], default='LIVRE', max_length=10)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Escola')),
                ('treinador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turmas', to='gerencia.treinador')),
            ],
        ),
    ]
