from django.db import models


class ReleaseNote(models.Model):

    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    release_note = models.BooleanField(default=False)

    class Meta:
        unique_together = (('owner', 'repo'),)
