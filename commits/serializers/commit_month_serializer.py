from rest_framework import serializers
from commits.models import CommitMonth

class CommitMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitMonth
        fields = '__all__'
