from django.db import models


class Commit(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
    date = models.DateField(default=None)