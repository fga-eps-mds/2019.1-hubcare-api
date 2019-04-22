from rest_framework import serializers
from issue_template_metric.models import IssueTemplates


class IssueTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueTemplates
        fields = '__all__'
