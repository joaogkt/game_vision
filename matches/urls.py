
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.matches_list, name='matches_list'),
    path('new/', views.matches_create, name='matches_create'),
    path('list/<int:pk>/', views.matches_detail, name='matches_detail'),
    path('<int:pk>/edit/', views.matches_update, name='matches_update'),
    path('<int:pk>/delete/', views.matches_delete, name='matches_delete'),

]
