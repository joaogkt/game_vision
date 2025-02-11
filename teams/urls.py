from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('list/', views.team_list, name='team_list'),
    path('create/', views.team_create, name='team_create'),
    path('<int:pk>/edit/', views.team_update, name='team_update'),
    path('<int:pk>/delete/', views.team_delete, name='team_delete'),
]