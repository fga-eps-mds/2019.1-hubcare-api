from django.db import models


class DifferentsAuthors(models.Model):
    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    differents_authors = models.IntegerField(default=0)

    class Meta:
        unique_together = (('owner', 'repo'),)
