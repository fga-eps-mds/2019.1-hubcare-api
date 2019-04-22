from django.db import models
from commits.models import Commit


class CommitWeek(models.Model):
    week = models.IntegerField()
    quantity = models.IntegerField()
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
