from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from contest import models

# we follow the convention that 'c' is context in the views

def contests_home(request):
    """
    Display active contests and general information.
    """
    c, template = {}, 'contest/contest_home.html'
    c['contests'] = models.Contest.objects.filter(published=True)
    return render(request, template, c)

def contest(request, pk):
    """
    Contest specific details.
    """
    c, template, pk = {}, 'contest/contest.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    return render(request, template, c)

def contest_lb(request, pk):
    """
    Leaderboard
    """
    c, template, pk = {}, 'contest/contest.html', int(pk)

    return render(request, template, c)

@login_required
def contest_submit(request, pk):
    """
    Submission page for contest
    """
    c, template, pk = {}, 'contest/contest.html', int(pk)
    return render(request, template, c)
