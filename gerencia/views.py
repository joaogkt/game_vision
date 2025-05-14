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



@login_required(login_url='login')
def registrar_presenca(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    jogadores = turma.player_set.all()

    if request.method == 'POST':
        presentes_ids = request.POST.getlist('presente')
        print("Presentes IDs:", presentes_ids)
        print("Jogadores:", jogadores)
        for jogador in jogadores:
            falta = str(jogador.id) not in presentes_ids
            print(f"Jogador: {jogador}, Falta: {falta}")
            presenca, created = Faltas.objects.update_or_create(
                aluno=jogador,
                data=date.today(),
                defaults={'falta': falta}
            )
            print(f"Presença: {presenca}, Criado: {created}")
            if created:
                if falta:
                    print(f"Falta registrada: {jogador} - {jogador.total_faltas}")
                    jogador.total_faltas += 1
                    jogador.save()
            else:
                print(f"Registro existente: {presenca} - {presenca.falta}")
                if presenca.falta:
                    jogador.total_faltas += 1
                    print(f"Falta registrada: {jogador} - {jogador.total_faltas}")
                    jogador.save()

        messages.success(request, "Presença registrada com sucesso!")
        return render(request, 'registrar_presenca.html', {
            'turma': turma,
            'jogadores': jogadores,
            'success': True
        })

    return render(request, 'registrar_presenca.html', {
        'turma': turma,
        'jogadores': jogadores
    })