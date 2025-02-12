
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.matches_list, name='matches_list'),
    path('new/', views.matches_create, name='matches_create')

]
