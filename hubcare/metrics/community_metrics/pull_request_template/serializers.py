from rest_framework import serializers
from pull_request_template.models import PullRequestTemplate


class PullRequestTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullRequestTemplate
        fields = '__all__'
