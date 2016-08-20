from django.db import models
from django.utils import timezone
from django.contrib.aut.models import User

now = timezone.now

class ScoreSchemes(models.Model):
    "Score schemes for cross validation"
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50, default='accuracy')

class Contest(models.Model):
    "Contest which is hosted"
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100)
    scoring = models.ForeignKey(ScoreSchemes, related_name='score_schemes_contest')
    tos = models.TextField(default='Do what you want after permission from the hosts of the contest.')

    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now)

    def is_live(self):
        "Is the contest live?"
        return self.start_time <= now() <= self.end_time


class Resource(models.Model):
    "Data File"
    def __str__(self):
        return self.csv_file.__str__()
    csv_file = models.FileField()
    contest = models.ForeignKey(Contest, related_name='contest_resource')
    test_file = models.FileField()

    public = models.BooleanField(default=True)

    def is_accessible(self, user):
        "Can this user access this resource?"
        contract_signed = Contract.objects.filter(user=user, contest=self.contest).count() > 0
        return (contract_signed and self.public)


class Contract(models.Model):
    "A contract of the user agreeing to the TOS of the contest"
    def __str__(self):
        return '{}_{}'.format(self.user, self.contest)
    user = models.ForeignKey(User, related_name='user_contract')
    contest = models.ForeignKey(Contest, related_name='contest_contract')
    tos = models.TextField(default='')

    stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'contest')

class Submission(models.Model):
    "A user's submission"
    def __str__(self):
        return '{}_{}_{}'.format(self.pk, self.user, self.contest)
    contract = models.ForeignKey(Contract, related_name='contract_submission')

    test_file = models.FileField()
    code_file = models.FileField()
    comment = models.TextField(default='')

    stamp = models.DateTimeField(auto_now_add=True)

    def score(self):
        "Score this submission"
        #TODO
        return 0
