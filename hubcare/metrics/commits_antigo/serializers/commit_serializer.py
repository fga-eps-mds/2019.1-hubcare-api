from rest_framework import serializers
from commits.models import Commit


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = '__all__'
