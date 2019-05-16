from django.db import models


class Repository(models.Model):
    owner = models.CharField(max_length=100)
    repo = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=None)
