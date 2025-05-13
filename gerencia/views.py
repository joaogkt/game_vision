from django.shortcuts import render, redirect, get_object_or_404
from .forms import TurmaForm, ResponsavelForm, TreinadorForm
from .models import Turma, Responsavel, Treinador
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from players.models import Player, Faltas
# Create your views here.
#Home
@login_required(login_url='login')
def gerencia_home(request):
    return render(request, 'gerencia_home.html')

#Responsavel
@login_required(login_url='login')
def gerencia_responsavel(request):
    responsaveis = Responsavel.objects.all()
    return render(request, 'gerencia_responsavel.html', {'responsaveis': responsaveis})

@login_required(login_url='login')
def gerencia_responsavel_create(request):
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerencia_responsavel')
    else:
        form = ResponsavelForm()
    return render(request, 'gerencia_responsavel_form.html', {'form': form})

@login_required(login_url='login')
def responsavel_update(request, pk):
    responsavel = get_object_or_404(Responsavel, pk=pk)
    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=responsavel)
        if form.is_valid():
            form.save()
            return redirect('gerencia_responsavel')
    else:
        form = ResponsavelForm(instance=responsavel)
    return render(request, 'gerencia_responsavel_form.html', {'form': form, 'responsavel': responsavel})

#Trenador
@login_required(login_url='login')
def gerencia_treinador(request):
    treinadores = Treinador.objects.all()
    return render(request, 'gerencia_treinador.html', {'treinadores': treinadores})

@login_required(login_url='login')
def gerencia_treinador_create(request):
    if request.method == 'POST':
        form = TreinadorForm(request.POST)
        print(form)
        if form.is_valid():
            print("ok")
            form.save()
            return redirect('gerencia_treinador')
    else:
        print("Not ok")
        form = TreinadorForm()
    return render(request, 'gerencia_treinador_form.html', {'form': form})

@login_required(login_url='login')
def gerencia_treinador_update(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    if request.method == 'POST':
        form = TreinadorForm(request.POST, instance=treinador)
        if form.is_valid():
            form.save()
            return redirect('gerencia_treinador')
    else:
        form = TreinadorForm(instance=treinador)
    return render(request, 'gerencia_treinador_form.html', {'form': form, 'treinador': treinador})

@login_required(login_url='login')
def gerencia_treinador_delete(request, pk):
    treinador = get_object_or_404(Treinador, pk=pk)
    treinador.delete()
    messages.success(request, "Treinador excluído com sucesso!")
    return redirect('gerencia_treinador')


#turmas
@login_required(login_url='login')
def turma_list(request):
    turmas = Turma.objects.all()
    return render(request, 'gerencia_turma.html', {'turmas': turmas})

@login_required(login_url='login')
def turma_create(request):
    if request.method == 'POST':
        form = TurmaForm(request.POST)
        print(form)
        if form.is_valid():
            print('ok')
            form.save()
            return redirect('gerencia_turma')
    else:
        print("Not ok ")
        form = TurmaForm()
    return render(request, 'gerencia_turma_form.html', {'form': form})

@login_required(login_url='login')
def turma_update(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('gerencia_turma')
    else:
        form = TurmaForm(instance=turma)
    return render(request, 'gerencia_turma_form.html', {'form': form, 'turma': turma})

@login_required(login_url='login')
def turma_delete(request, pk):
    turma = get_object_or_404(Turma, pk=pk)
    turma.delete()
    messages.success(request, "Turma excluído com sucesso!")
    return redirect('gerencia_turma') 



#presenca
@login_required(login_url='login')
def registrar_presenca(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    jogadores = Player.objects.filter(turma=turma)

    if request.method == 'POST':
        presentes_ids = request.POST.getlist('presente')
        try:
            for jogador in jogadores:
                falta = jogador.id not in [int(id) for id in presentes_ids]
                Faltas.objects.create(aluno=jogador, turma=turma, data=date.today(), falta=falta)
            messages.success(request, 'Presença registrada com sucesso!')
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao registrar presença: {str(e)}')

        return redirect('registrar_presenca', turma_id=turma.id)

    return render(request, 'registrar_presenca.html', {'turma': turma, 'jogadores': jogadores})