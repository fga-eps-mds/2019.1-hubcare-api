from rest_framework import serializers
from community.models.issue_templates_model import IssueTemplates


class IssueTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueTemplates
        fields = '__all__'
