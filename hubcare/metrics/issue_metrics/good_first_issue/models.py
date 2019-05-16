from django.db import models


class GoodFirstIssue(models.Model):
    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    total_issues = models.IntegerField(default=0)
    good_first_issue = models.IntegerField(default=0)
