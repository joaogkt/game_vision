from django.shortcuts import render, redirect
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