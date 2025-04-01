
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/register/', views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/verify/', views.verify, name='verify'),
    path('accounts/resend-code/', views.verify, name='verify'),
    path('feedback/', views.feedback, name='feedback'),
]
