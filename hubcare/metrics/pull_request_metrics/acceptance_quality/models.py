from django.db import models


class PullRequestQuality(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    date = models.DateTimeField(default=None)
    metric = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = (('owner', 'repo'),)
