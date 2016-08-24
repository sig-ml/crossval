from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from contest import models, forms

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
    c['resources'] = models.Resource.objects.filter(public=True,
            contest=c['contest'])
    c['signed_contract'] = False
    if request.user.is_authenticated():
        c['signed_contract'] = models.Contract.objects.filter(user=request.user, contest=c['contest']).count() > 0
    return render(request, template, c)

def contest_lb(request, pk):
    """
    Leaderboard
    """
    c, template, pk = {}, 'contest/contest_lb.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    c['pk'] = c['contest'].pk

    # rankings
    contracts = models.Contract.objects.filter(contest=c['contest'])
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
    c, template, pk = {}, 'contest/contest_submit.html', int(pk)
    print(pk, 'called function')
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    print('obtained and failed contract')
    contract_exists = models.Contract.objects.filter(contest=c['contest'], user=request.user).count() > 0
    if contract_exists:
        print('obtained and failed')
        contract = get_object_or_404(models.Contract,
                contest=c['contest'], user=request.user)
        c['pk'] = c['contest'].pk
        c['submit_form'] = forms.SubmissionForm()
        if request.method == 'POST':
            form = forms.SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                sub = form.save(commit=False)
                sub.contract = contract
                sub.save()
            else:
                c['submit_form'] = form
        return render(request, template, c)
    else:
        print('Contract not signed')
        return redirect('contract', pk)


@login_required
def contract(request, pk):
    "Sign the contract"
    c, template, pk = {}, 'contest/contest_contract.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    c['contract_form'] = forms.ContractForm()
    if request.method == 'POST':
        contract_form = forms.ContractForm(request.POST)
        if contract_form.is_valid():
            contract = contract_form.save(commit=False)
            contract.contest = c['contest']
            contract.user = request.user
            contract.tos = c['contest'].tos
            try:
                contract.save()
            except:
                pass
            return redirect('contest', pk)
        else:
            c['contract_form'] = contract_form
    return render(request, template, c)


@login_required
def contest_resource(request, pk):
    "Return permissions for the contest resource"
    pk = int(pk)
    resource = get_object_or_404(models.Resource, pk=pk)
    if resource.public and resource.is_contract_signed(request.user):
        pass
        # TODO: complete this Accel-redirect?
