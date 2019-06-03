from django.db import models


class DifferentsAuthors(models.Model):
    owner = models.CharField(max_length=30)
    repo = models.CharField(max_length=30)
    commits = models.CharField(max_length=150)
    date = models.DateField(max_length=150)

    class Meta:
        unique_together = (('owner', 'repo'),)
