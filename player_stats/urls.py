
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.player_stats_list, name='player_stats_list'),
    path('new/', views.player_stats_list, name='player_stats_create'),
    path('list/<int:pk>/', views.player_stats_list, name='player_stats__detail'),
    path('<int:pk>/edit/', views.player_stats_list, name='player_stats__update'),
    path('<int:pk>/delete/', views.player_stats_list, name='player_stats__delete'),
]