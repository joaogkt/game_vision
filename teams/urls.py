from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('list/', views.teams_list, name='teams_list'),


]