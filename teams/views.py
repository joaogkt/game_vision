from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Team
from players.models import Player
from .forms import TeamForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login')
def team_list(request):
    teams = Team.objects.all()
    player = Player.objects.all()
    return render(request, 'team_list.html', {'teams': teams, 'players': player})


@login_required(login_url='login')
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'team_detail.html', {'team': team})


@login_required(login_url='login')
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'team_form.html', {'form': form})

@login_required(login_url='login')
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm(instance=team)
    return render(request, 'team_form.html', {'form': form})


@login_required(login_url='login')
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        team.delete()
        return redirect('team_list')
    return render(request, 'team_confirm_delete.html', {'team': team})
