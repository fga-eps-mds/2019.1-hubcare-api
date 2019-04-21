from rest_framework import serializers
from issues.models.good_first_issue_model import GoodFirstIssue


class GoodFirstIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodFirstIssue
        fields = '__all__'
