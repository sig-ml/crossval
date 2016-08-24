from django.forms import ModelForm
from contest import models


class SubmissionForm(ModelForm):
    class Meta:
        model = models.Submission
        exclude = ['contract', 'score', 'valid']

