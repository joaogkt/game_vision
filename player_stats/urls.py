
from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('list/', views.player_stats_list, name='player_stats_list'),
    path('new/', views.player_stats_create, name='player_stats_create'),
    path('list/<int:pk>/', views.player_stats_detail, name='player_stats_detail'),
    path('<int:pk>/edit/', views.player_stats_update, name='player_stats_update'),
    path('<int:pk>/delete/', views.player_stats_delete, name='player_stats_delete'),
    path('desempenho_geral/', views.desempenho_geral, name='player_stats_total'),
    path('desempenho_geral/graficos', views.desempenho_graficos, name='player_stats_graficos'),
    path('desempenho_geral/comparar/<int:pk1>/<int:pk2>', views.comparar_jogadores, name='comparar_jogadores'),
    path('desempenho_jogador/<int:jogador_id>/', views.desempenho_jogador, name='desempenho_partida'),



]
