from django.db import models

# Create your models here.
class Readme(models.Model):
    owner = models.CharField(max_length=30)
    repo = models.CharField(max_length=30)
    has_readme = models.BooleanField()
    # date