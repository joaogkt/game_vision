from django.shortcuts import render, redirect, get_object_or_404
from .forms import MatchesForm
from .models import Matches

# Create your views here.
def matches_list(request):
    matches = Matches.objects.all()
    return render(request, 'matches_list.html', {'matches': matches})

def matches_create(request):
    if request.method == "POST":
        form = MatchesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matches_list')
    else:
        form = MatchesForm()
    return render(request, 'matches_form.html', {'form': form})


def matches_detail(request, pk):
    matches = get_object_or_404(Matches, pk=pk)
    return render(request, 'matches_detail.html', {'matches': matches})

def matches_delete(request, pk):
    matches = get_object_or_404(Matches, pk=pk)
    if request.method == "POST":
        matches.delete()
        return redirect('matches_list')
    return render(request, 'matches_confirm_delete.html', {'matches': matches})
