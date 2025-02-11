
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.player_list, name='player_list'),
    path('list/<int:pk>/', views.player_detail, name='player_detail'),
    path('new/', views.player_create, name='player_create'),
    path('<int:pk>/edit/', views.player_update, name='player_update'),
    path('<int:pk>/delete/', views.player_delete, name='player_delete'),
]
