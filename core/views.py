from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from .models import CustomUser
# from .forms import CustomUserCreationForm
# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')
# def login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         usuario = authenticate(request, username=email, password=password)
#         if usuario is not None:
#             login(request, usuario)
#             return redirect('index')
#         else:
#             form_login = AuthenticationForm()
#     else:
#         form_login = AuthenticationForm()
#     return render(request, 'login.html', {'form_login': form_login})

# def register(request):
#     if request.method == "POST":
#         form_usuario = CustomUserCreationForm(request.POST)
#         if form_usuario.is_valid():
#             form_usuario.save()
#             return redirect('index')
#     else:
#         form_usuario = CustomUserCreationForm()
#     return render(request, 'register.html', {'form_usuario': form_usuario})
