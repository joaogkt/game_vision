from django.shortcuts import render, redirect, get_object_or_404
from .forms import MatchesForm
from .models import Matches
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from core.views import is_admin

# Create your views here.
@login_required(login_url='login')
def matches_list(request):
    matches = Matches.objects.all()
    return render(request, 'matches_list.html', {'matches': matches})

@user_passes_test(is_admin)
@login_required(login_url='login')
def matches_create(request):
    if request.method == "POST":
        form = MatchesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matches_list')
    else:
        form = MatchesForm()
    return render(request, 'matches_form.html', {'form': form})

@user_passes_test(is_admin)
@login_required(login_url='login')
def matches_detail(request, pk):
    matches = get_object_or_404(Matches, pk=pk)
    return render(request, 'matches_detail.html', {'matches': matches})

@user_passes_test(is_admin)
@login_required(login_url='login')
def matches_delete(request, pk):
    matches = get_object_or_404(Matches, pk=pk)
    if request.method == "POST":
        matches.delete()
        return redirect('matches_list')
    return render(request, 'matches_confirm_delete.html', {'matches': matches})

@user_passes_test(is_admin)
@login_required(login_url='login')
def matches_update(request, pk):
    match = get_object_or_404(Matches, pk=pk)
    if request.method == 'POST':
        form = MatchesForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('matches_detail', pk=match.pk)
    else:
        form = MatchesForm(instance=match)

    return render(request, 'matches_form.html', {'form': form})