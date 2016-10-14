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
    users = [(i.public_max_score, i)
              for i in contracts]
    users.sort(reverse=(not c['contest'].reverse_lb))
    c['players'] = users

    return render(request, template, c)

@login_required
def contest_submit(request, pk):
    """
    Submission page for contest
    """
    c, template, pk = {}, 'contest/contest_submit.html', int(pk)
    c['contest'] = get_object_or_404(models.Contest, pk=pk)
    contract_exists = models.Contract.objects.filter(contest=c['contest'], user=request.user).count() == 1

    if contract_exists:
        contract = get_object_or_404(models.Contract,
                contest=c['contest'], user=request.user)
        c['past_submissions'] = models.Submission.objects.filter(contract=contract).order_by('-stamp') #TODO: get only top n
        c['pk'] = c['contest'].pk
        c['submit_form'] = forms.SubmissionForm()

        sub_limit = c['contest'].max_submissions_per_day
        c['sub_limit_reached'] = False
        if sub_limit != -1:
            # TODO: submissions must be counted in today's date
            sub_done = models.Submission.objects.filter(contract=contract, valid=True).count()
            print(sub_limit, '*'*10)  # TODO: remove this or add a proper logging mechanism
            if sub_done >= sub_limit:
                c['submit_form'] = None
                c['sub_limit_reached'] = True


        if request.method == 'POST' and not c['sub_limit_reached']:
            form = forms.SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                sub = form.save(commit=False)
                sub.contract = contract
                sub.save()
                sub.calculate_score()
            else:
                c['submit_form'] = form
        return render(request, template, c)
    else:
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
