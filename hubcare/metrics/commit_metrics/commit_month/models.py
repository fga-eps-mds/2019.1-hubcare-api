from django.db import models


class CommitMonth(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    total_commits = models.IntegerField(default=0)
    commits_high_score = models.IntegerField()
    commits_week = models.TextField()
    commits_last_period = models.IntegerField(default=0)

    class Meta:
        unique_together = (('owner', 'repo'),)
