from django.db import models


class RepositoryDescription(models.Model):
    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    description = models.BooleanField(default=False)
    date = models.DateTimeField(default=None)
