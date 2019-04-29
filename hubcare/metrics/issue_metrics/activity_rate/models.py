from django.db import models


class ActivityRateIssue(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    date = models.DateTimeField(default=None)
    activity_rate = models.DecimalField(max_digits=5, decimal_places=2)
    activity_rate_15_days = models.DecimalField(max_digits=5, decimal_places=2)
    activity_rate_15_days_metric = models.DecimalField(max_digits=5,
                                                       decimal_places=2)
