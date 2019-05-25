from django.db import models


class IssueTemplate(models.Model):

    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    issue_template = models.BooleanField(default=False)

    class Meta:
        unique_together = (('owner', 'repo'),)
