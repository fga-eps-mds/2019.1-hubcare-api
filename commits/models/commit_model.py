from django.db import models


class Commit(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    date = models.DateField(default=None)


class CommitDay(models.Model):
    date = models.DateField(default=None)
    quantity = models.IntegerField()
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)


class CommitWeek(models.Model):
    week = models.IntegerField()
    quantity = models.IntegerField()
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    