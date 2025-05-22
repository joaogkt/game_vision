from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/', views.gerencia_home, name='gerencia_home'),

    
    path('turma/create/', views.turma_create, name='gerencia_turma_create'),
    path('turma/', views.turma_list, name='gerencia_turma'),
    path('turma/<int:pk>/', views.turma_update, name='turma_update'),
    path('<int:pk>/delete/', views.turma_delete, name='turma_delete'),


    path('responsavel/', views.gerencia_responsavel, name='gerencia_responsavel'),
    path('<int:pk>/delete', views.responsavel_delete, name='responsavel_delete'),
    path('responsavel/<int:pk>', views.responsavel_update, name='responsavel_update'),

    path('responsavel/create/', views.gerencia_responsavel_create, name='gerencia_responsavel_create'),


    path('treinador/', views.gerencia_treinador, name='gerencia_treinador'),
    path('treinador/create/', views.gerencia_treinador_create, name='gerencia_treinador_create'),
    path('treinador/<int:pk>', views.gerencia_treinador_update, name='gerencia_treinador_update'),
    path('treinador/<int:pk>/delete', views.gerencia_treinador_delete, name='gerencia_treinador_delete'),


    path('turma/<int:turma_id>/presenca/', views.registrar_presenca, name='registrar_presenca'),

    path('relatorios/', views.gerencia_relatorios, name='gerencia_relatorios'),
    path('importar/', views.import_data, name='import_data'),
    path('export/', views.export_data, name='export_data'),


    
]
