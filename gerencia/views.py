from django.shortcuts import render, redirect, get_object_or_404
from .forms import TurmaForm, ResponsavelForm, TreinadorForm
from .models import Turma, Responsavel, Treinador
from django.contrib.auth.decorators import login_required

# Create your views here.
#Home
def gerencia_home(request):
    return render(request, 'gerencia_home.html')

#Responsavel
def gerencia_responsavel(request):
    return render(request, 'gerencia_responsavel.html')

def gerencia_responsavel_create(request):
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia_responsavel')
    else:
        form = ResponsavelForm()
    return render(request, 'gerencia_responsavel_create.html', {'form': form})

def gerencia_responsavel_update(request, pk):
    responsavel = get_object_or_404(Responsavel, pk=pk)
    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=responsavel)
        if form.is_valid():
            form.save()
            return redirect('gerencia_responsavel')
    else:
        form = ResponsavelForm(instance=responsavel)
    return render(request, 'gerencia_responsavel_update.html', {'form': form, 'responsavel': responsavel})

#Trenador
def gerencia_treinador(request):
    return render(request, 'gerencia_treinador.html')

def gerencia_treinador_create(request):
    if request.method == 'POST':
        form = TreinadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia_treinador')
    else:
        form = TreinadorForm()
    return render(request, 'gerencia_treinador_create.html', {'form': form})

def gerencia_treinador_update(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    if request.method == 'POST':
        form = TreinadorForm(request.POST, instance=treinador)
        if form.is_valid():
            form.save()
            return redirect('gerencia_treinador')
    else:
        form = TreinadorForm(instance=treinador)
    return render(request, 'gerencia_treinador_update.html', {'form': form, 'treinador': treinador})


#turmas
def gerencia_turma(request):
    return render(request, 'gerencia_turma.html')

def gerencia_turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia_turma')
    else:
        form = TurmaForm()
    return render(request, 'gerencia_turma_create.html', {'form': form})

def gerencia_turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('gerencia_turma')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'gerencia_turma_update.html', {'form': form, 'turma': turma})
