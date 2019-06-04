from rest_framework import serializers
from good_first_issue.models import GoodFirstIssue


class GoodFirstIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodFirstIssue
        fields = [
            'total_issues',
            'good_first_issue',
            'good_first_issue_rate',
            'good_first_issue_max_rate'
        ]
