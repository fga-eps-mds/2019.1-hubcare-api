from django.db import models


class CommitMonth(models.Model):
    owner = models.CharField(max_length=150)
    repo = models.CharField(max_length=150)
