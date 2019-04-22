from rest_framework import serializers
from good_first_issue.models import GoodFirstIssue


class GoodFirstIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodFirstIssue
        fields = '__all__'
