from django.db import models


class IssueTemplate(models.Model):

    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    issue_templates = models.BooleanField(default=False)
    date_time = models.DateTimeField(default=None)
