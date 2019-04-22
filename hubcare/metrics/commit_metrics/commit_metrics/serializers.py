from rest_framework import serializers
from commit_metrics.models import Commit


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = '__all__'
