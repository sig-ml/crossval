import pandas as pd
from sklearn import metrics

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

now = timezone.now

class Contest(models.Model):
    """
    Contest which is hosted
    """
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100)
    tos = models.TextField(default='Do what you want after permission from the hosts of the contest.')
    ground_truth = models.FileField(upload_to='ground_truth/')
    max_submissions_per_day = models.IntegerField(default=50)
    metric = models.CharField(default='accuracy', max_length=50)
    reverse_lb = models.BooleanField(default=True, help_text='Leaderboard must be sorted lowest metric first?')

    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now)
    published = models.BooleanField(default=False)

    check_script = models.TextField(default='#given_path, ground_path, pandas as pd, metrics, are variables available',
                    help_text='script to check and set the score variable to an appropriate value')

    def is_live(self):
        "Is the contest live?"
        return self.start_time <= now() <= self.end_time


class Resource(models.Model):
    """
    Data Files, mostly csvs
    """
    def __str__(self):
        return self.csv_file.__str__()
    csv_file = models.FileField(upload_to='resource/')
    contest = models.ForeignKey(Contest, related_name='contest_resource')
    public = models.BooleanField(default=True)

    def is_contract_signed(self, user):
        "Has this user signed the contract?"
        contract_signed = Contract.objects.filter(user=user, contest=self.contest).count() > 0
        return contract_signed


class Contract(models.Model):
    "A contract of the user agreeing to the TOS of the contest"
    def __str__(self):
        return '{}_{}'.format(self.user, self.contest)
    user = models.ForeignKey(User, related_name='user_contract')
    contest = models.ForeignKey(Contest, related_name='contest_contract')
    tos = models.TextField(default='')  # Terms of service
    nick = models.CharField(max_length=50)  #TODO: can clash with other users in the contest
    _last_submission_stamp = models.DateTimeField(default=now)
    public_max_score = models.FloatField(default=0.0)

    stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'contest')


class Submission(models.Model):
    "A user's submission"
    def __str__(self):
        return '{}_{}'.format(self.pk, self.contract)
    contract = models.ForeignKey(Contract, related_name='contract_submission')
    test_file = models.FileField(upload_to='submission/csv/', help_text='the submission csv file')
    code_file = models.FileField(upload_to='submission/code/', help_text='The program used to generate the file')
    comment = models.TextField(default='', help_text='Write something to help you remember later on what you did')
    score = models.FloatField(default=None, null=True)
    valid = models.BooleanField(default=False)

    stamp = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        "Calculate the score of the given submission -> if score was calculated, score"
        check_script = self.contract.contest.check_script

        global_dict = {'pd': globals()['pd'],
                'metrics': globals()['metrics'],
                'given_path': self.test_file.path,
                'ground_path': self.contract.contest.ground_truth.path
                }
        local_dict = {}
        try:
            exec(check_script, global_dict, local_dict)  # this script is supposed to set the score value
        except:
            score = None
        else:
            if 'score' in global_dict.keys():
                score = global_dict['score']
            elif 'score' in local_dict.keys():
                score = local_dict['score']
            self.score = score
            self.save()
            if self.contract.public_max_score < score:
                self.contract.public_max_score = score
                self.contract.save()
        return score
