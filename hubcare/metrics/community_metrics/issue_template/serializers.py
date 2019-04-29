from rest_framework import serializers
from issue_template.models import IssueTemplate


class IssueTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueTemplate
        fields = '__all__'
