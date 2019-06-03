from django.db import models


class HelpWanted(models.Model):
    owner = models.CharField(max_length=100)
    repo = models.CharField(max_length=100)
    total_issues = models.IntegerField(default=0)
    help_wanted_rate = models.DecimalField(max_digits=5, decimal_places=2)
    help_wanted_issues = models.IntegerField()

    class Meta:
        unique_together = (('owner', 'repo'),)
