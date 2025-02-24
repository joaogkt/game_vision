from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage

def send_email(remetente, code):
    email = EmailMessage(
        'Codigo de autenticação',
        code,
        'game.vision.udf@gmail.com',
        [remetente],
        fail_silently=False,
    )
    email.send()


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            form_login = AuthenticationForm()
            error_message = "Credenciais inválidas. Tente novamente."
            return render(request, 'login.html', {
                'form_login': form_login,
                'error_message': error_message,
            })
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'form_login': form_login})

def register(request):
    if request.method == "POST":
        form_usuario = CustomUserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
        else:
            for error in form_usuario.errors.get("password1", []):
                messages.error(request, error)
    else:
        form_usuario = CustomUserCreationForm()
    return render(request, 'register.html', {'form_usuario': form_usuario})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')