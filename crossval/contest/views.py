from django.shortcuts import render
from contest import models

def contests_home(request):
    """
    Display active contests and general information.
    """
    pass

def contest(request, pk):
    """
    Contest specific details.
    """
    pass

def contest_lb(request, pk):
    """
    Leaderboard
    """
    pass

def contest_submit(request, pk):
    """
    Submission page for contest
    """
    pass
