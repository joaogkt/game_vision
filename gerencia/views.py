from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import TurmaForm, ResponsavelForm, TreinadorForm
from .models import Turma, Responsavel, Treinador
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from players.models import Player, Faltas
import csv
import io
from player_stats.models import PlayerStats
from matches.models import Matches
from teams.models import Team
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

def responsavel_delete(request, pk):
    responsavel = get_object_or_404(Responsavel, pk=pk)
    responsavel.delete()
    messages.success(request, "Responsável excluído com sucesso!")
    return redirect('gerencia_responsavel')

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
                turma=turma,
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

@login_required(login_url='login')
def gerencia_relatorios(request):
    return render(request, 'gerencia_relatorios.html')


def import_data(request):
    if request.method == 'POST':
        table = request.POST.get('table')
        csv_file = request.FILES.get('file')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Por favor, envie um arquivo CSV.')
            return redirect('import_data')

        try:
            data_set = csv_file.read().decode('utf-8')
            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)

            count = 0

            if table == 'responsavel':
                for row in reader:
                    Responsavel.objects.create(
                        nome=row['nome'],
                        email=row['email'],
                        telefone=row['telefone'],
                        data_nascimento=row.get('data_nascimento') or None,
                        cpf=row['cpf']
                    )
                    count += 1

            elif table == 'treinador':
                for row in reader:
                    Treinador.objects.create(
                        nome=row['nome'],
                        email=row['email'],
                        telefone=row['telefone'],
                        data_nascimento=row.get('data_nascimento') or None,
                        cpf=row['cpf']
                    )
                    count += 1

            elif table == 'team':
                for row in reader:
                    Team.objects.create(
                        name=row['name'],
                        city=row['city'],
                        country=row['country'],
                        founded_year=row.get('founded_year') or 1900
                    )
                    count += 1


            elif table == 'turma':
                for row in reader:
                    Turma.objects.create(
                        nome=row['nome'],
                        team=Team.objects.get(name=row['team']),
                        treinador=Treinador.objects.get(nome=row['treinador']),
                        horario_treino=row['horario_treino'],
                        categoria=row.get('categoria') or 'LIVRE'
                    )
                    count += 1

            elif table == 'matches':
                for row in reader:
                    Matches.objects.create(
                        local=row['local'],
                        time_casa=Team.objects.get(name=row['time_casa']),
                        time_fora=Team.objects.get(name=row['time_fora']),
                        placar_casa=row['placar_casa'],
                        placar_fora=row['placar_fora'],
                        data_partida=row.get('data_partida') or None,
                        tipo_competicao=row['tipo_competicao']
                    )
                    count += 1
            elif table == 'playerstats':
                for row in reader:
                    try:
                        nome_jogador = row['jogador_nome'].strip()
                        nome_partida = row['partida'].strip()

                        first_name, last_name = nome_jogador.split(' ', 1)
                        jogador = Player.objects.get(first_name=first_name, last_name=last_name)

                        partida = None
                        for match in Matches.objects.all():
                            if str(match) == nome_partida:
                                partida = match
                                break
                        if not partida:
                            raise Matches.DoesNotExist(f"Partida '{nome_partida}' não encontrada.")

                        PlayerStats.objects.create(
                            jogador=jogador,
                            jogo=partida,
                            minutos_jogados=int(row['minutos_jogados']),
                            gols=int(row['gols']),
                            assistencia=int(row['assistencia']),
                            passes_certos=int(row['passes_certos']),
                            passes_errados=int(row['passes_errados']),
                            desarmes=int(row['desarmes']),
                            cartao_vermelho=int(row['cartao_vermelho']),
                            cartao_amarelo=int(row['cartao_amarelo']),
                            nota=float(row['nota'])
                        )
                    except (Player.DoesNotExist, Matches.DoesNotExist) as e:
                        messages.error(request, f"Erro: {e}")
                        continue

            elif table == 'player':
                for row in reader:
                    Player.objects.create(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        birth_date=row['birth_date'],
                        nationality=row['nationality'],
                        position=row['position'],
                        team=Team.objects.get(name=row['team']),
                        status=row.get('status') or 'ativo'
                    )
                    count += 1

            else:
                messages.error(request, 'Tabela inválida selecionada.')
                return redirect('import_data')

            messages.success(request, f'{count} registros importados com sucesso!')
            return redirect('import_data')

        except Exception as e:
            messages.error(request, f'Erro ao importar dados: {str(e)}')
            return redirect('import_data')

    return render(request, 'import_data.html')


def export_data(request):
    if request.method == 'POST':
        table = request.POST.get('table')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{table}.csv"'

        writer = csv.writer(response)

        if table == 'player':
            writer.writerow(['first_name', 'last_name', 'birth_date', 'nationality', 'position', 'team', 'status'])
            for obj in Player.objects.all():
                writer.writerow([
                    obj.first_name,
                    obj.last_name,
                    obj.birth_date,
                    obj.nationality.name if obj.nationality else '',
                    obj.position,
                    obj.team.name if obj.team else '',
                    obj.status
                ])
                
        elif table == 'playerstats':
            writer.writerow([
                'jogador', 'jogo', 'minutos_jogados', 'gols', 'assistencia', 
                'passes_certos', 'passes_errados', 'desarmes', 
                'cartao_vermelho', 'cartao_amarelo', 'nota'
            ])
            for obj in PlayerStats.objects.all():
                writer.writerow([
                    f"{obj.jogador.first_name} {obj.jogador.last_name}",
                    str(obj.jogo), 
                    obj.minutos_jogados,
                    obj.gols,
                    obj.assistencia,
                    obj.passes_certos,
                    obj.passes_errados,
                    obj.desarmes,
                    obj.cartao_vermelho,
                    obj.cartao_amarelo,
                    obj.nota
                ])

        elif table == 'responsavel':
            writer.writerow(['nome', 'email', 'telefone', 'data_nascimento', 'cpf'])
            for obj in Responsavel.objects.all():
                writer.writerow([
                    obj.nome,
                    obj.email,
                    obj.telefone,
                    obj.data_nascimento,
                    obj.cpf
                ])

        elif table == 'treinador':
            writer.writerow(['nome', 'email', 'telefone', 'data_nascimento', 'cpf'])
            for obj in Treinador.objects.all():
                writer.writerow([
                    obj.nome,
                    obj.email,
                    obj.telefone,
                    obj.data_nascimento,
                    obj.cpf
                ])

        elif table == 'turma':
            writer.writerow(['nome', 'team', 'treinador', 'horario_treino', 'categoria'])
            for obj in Turma.objects.all():
                writer.writerow([
                    obj.nome,
                    obj.team.name if obj.team else '',
                    obj.treinador.nome if obj.treinador else '',
                    obj.horario_treino,
                    obj.categoria
                ])

        elif table == 'team':
            writer.writerow(['name', 'city', 'country', 'founded_year'])
            for obj in Team.objects.all():
                writer.writerow([
                    obj.name,
                    obj.city,
                    obj.country.name if obj.country else '',
                    obj.founded_year
                ])

        elif table == 'matches':
            writer.writerow(['local', 'time_casa', 'time_fora', 'placar_casa', 'placar_fora', 'data_partida', 'tipo_competicao'])
            for obj in Matches.objects.all():
                writer.writerow([
                    obj.local,
                    obj.time_casa.name if obj.time_casa else '',
                    obj.time_fora.name if obj.time_fora else '',
                    obj.placar_casa,
                    obj.placar_fora,
                    obj.data_partida,
                    obj.tipo_competicao
                ])
        elif table == 'faltas':
            writer.writerow([
                'jogador', 'turma', 'data', 'falta'
            ])
            for obj in Faltas.objects.all():
                writer.writerow([
                    f"{obj.aluno.first_name} {obj.aluno.last_name}",
                    str(obj.turma.nome), 
                    obj.data,
                    obj.falta,
                ])

        else:
            response.write('Tabela não encontrada.')
        
        return response

    return render(request, 'export_data.html')