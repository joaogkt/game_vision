from django.shortcuts import render, get_object_or_404, redirect
from .models import Player
from .forms import PlayerForm
import os

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player_list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'player_detail.html', {'player': player})

def player_create(request):
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('player_list')
    else:
        form = PlayerForm()
    return render(request, 'player_form.html', {'form': form})

def player_update(request, pk):
    player = get_object_or_404(Player, pk=pk)
    old_photo = player.photo.path if player.photo else None

    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            # if form.cleaned_data.get('remove_photo'):
            #     if old_photo and os.path.isfile(old_photo):
            #         os.remove(old_photo)
            #     player.photo = None

            # elif 'photo' in request.FILES:
            #     if old_photo and os.path.isfile(old_photo):
            #         os.remove(old_photo)

            form.save()
            return redirect('player_detail', pk=player.pk)
    else:
        form = PlayerForm(instance=player)

    return render(request, 'player_form.html', {'form': form})
    # player = get_object_or_404(Player, pk=pk)
    # if request.method == "POST":
    #     form = PlayerForm(request.POST, request.FILES, instance=player)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('player_detail', pk=pk)
    # else:
    #     form = PlayerForm(instance=player)
    # return render(request, 'player_form.html', {'form': form})

def player_delete(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if request.method == "POST":
        player.delete()
        return redirect('player_list')
    return render(request, 'player_confirm_delete.html', {'player': player})
