from django.db import models


class HubcareAPI(models.Model):

    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    active_indicator = models.FloatField()
    welcoming_indicator = models.FloatField()
    support_indicator = models.FloatField()
