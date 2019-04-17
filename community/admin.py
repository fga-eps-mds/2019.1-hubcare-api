from django.contrib import admin
from community.models.pr_template_model import PullRequestTemplate
from community.models.license_model import License

# Register your models here.
admin.site.register(PullRequestTemplate)
admin.site.register(License)
