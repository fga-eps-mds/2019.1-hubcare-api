from django.db import models
from commit_metrics.models import Commit


class CommitWeek(models.Model):
    week = models.IntegerField()
    quantity = models.IntegerField()
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
