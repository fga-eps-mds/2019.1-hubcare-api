from django.db import models


class ReleaseNote(models.Model):

    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)
    have_realease_note = models.BooleanField(default=False)
    date = models.DateTimeField(default=None)

    class Meta:
        unique_together = (('owner', 'repo'),)
