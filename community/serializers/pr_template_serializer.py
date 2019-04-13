from rest_framework import serializers
from community.models.pr_template_model import PullRequestTemplate


class PullRequestTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullRequestTemplate
        fields = '__all__'
