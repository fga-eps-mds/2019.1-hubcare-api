from rest_framework import serializers
from pr_template_metric.models import PullRequestTemplate


class PullRequestTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullRequestTemplate
        fields = '__all__'
