from django.forms import ModelForm
from contest import models


class SubmissionForm(ModelForm):
    class Meta:
        model = models.Submission
        exclude = ['contract', 'score', 'valid']

class ContractForm(ModelForm):
    class Meta:
        model = models.Contract
        exclude = ['user', 'contest', 'tos', '_last_submission_stamp', 'public_max_score', 'stamp']
