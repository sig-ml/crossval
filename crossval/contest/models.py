from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

now = timezone.now

class ScoreSchemes(models.Model):
    """
    Score schemes for cross validation
    """
    def __str__(self):
        return self.name
    name = models.CharField(max_length=50, default='accuracy')
    lower_is_better = models.BooleanField(default=True, help_text='Is a lower score better')

class Contest(models.Model):
    """
    Contest which is hosted
    """
    def __str__(self):
        return self.title
    title = models.CharField(max_length=100)
    scoring = models.ForeignKey(ScoreSchemes, related_name='score_schemes_contest')
    tos = models.TextField(default='Do what you want after permission from the hosts of the contest.')
    ground_truth = models.FileField(upload_to='ground_truth/')
    max_submissions_per_day = models.IntegerField(default=50)

    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(default=now)
    published = models.BooleanField(default=False)

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

    def get_score(self):
        last_sub = Submission.objects.filter(valid=True)


class Submission(models.Model):
    "A user's submission"
    def __str__(self):
        return '{}_{}_{}'.format(self.pk, self.user, self.contest)
    contract = models.ForeignKey(Contract, related_name='contract_submission')
    test_file = models.FileField(upload_to='submission/csv/')
    code_file = models.FileField(upload_to='submission/code/')
    comment = models.TextField(default='')
    score = models.FloatField(default=None, null=True)
    valid = models.BooleanField(default=False)

    stamp = models.DateTimeField(auto_now_add=True)

    def __check_valid(self):
        pass

    def __check_public_score(self):
        pass

    def __check_private_score(self):
        #TODO
        # check if valid
        # calculate score
        return 0
