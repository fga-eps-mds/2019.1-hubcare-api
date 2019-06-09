from django.db import models


class ActivityRateIssue(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    activity_max_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                            default=0.00)
    activity_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                        default=0.00)
    active_issues = models.IntegerField(default=0)
    dead_issues = models.IntegerField(default=0)

    class Meta:
        unique_together = (('owner', 'repo'),)
