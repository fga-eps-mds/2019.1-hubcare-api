from django.db import models

# Create your models here.

class HelpWanted(models.Model):
    total_issues = models.IntegerField(default=0)
    help_wanted_issues = models.IntegerField(default=0)
    