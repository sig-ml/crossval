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
    c['pk'] = c['contest'].pk
    c['resources'] = models.Resource.filter(public=True,
            contest=c['contest'])
    return render(request, template, c)

def contest_lb(request, pk):
    """
    Leaderboard
    """
    c, template, pk = {}, 'contest/contest.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    c['pk'] = c['contest'].pk

    # rankings
    contracts = models.Contract.filter(contest=c['contest'])
    users = [(i.get_score(), i.nick)
              for i in contracts]
    users.sort(reverse=(not c['contest'].scoring.lower_is_better))
    c['players'] = [player[1] for player in users]

    return render(request, template, c)

@login_required
def contest_submit(request, pk):
    """
    Submission page for contest
    """
    c, template, pk = {}, 'contest/contest.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    c['pk'] = c['contest'].pk
    # TODO: forms
    return render(request, template, c)


@login_required
def contest_resource(request, pk):
    "Return permissions for the contest resource"
    pk = int(pk)
    resource = get_object_or_404(models.Resource, pk=pk)
    if resource.public and resource.is_contract_signed(request.user):
        pass
        # TODO: complete this Accel-redirect?

