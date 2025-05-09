from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.gerencia_home, name='gerencia_home'),
    path('responsavel/', views.gerencia_responsavel, name='gerencia_responsavel'),
    path('treinador/', views.gerencia_treinador, name='gerencia_treinador'),
    path('turma/', views.gerencia_turma, name='gerencia_turma'),
]
