from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('v1/estatisticas/', views.api_estatisticas_jogadores, name='api_estatisticas_jogadores'),


]