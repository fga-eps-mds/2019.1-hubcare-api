from rest_framework import serializers
from commits.models.contributors_models import DifferentsAuthors


class DifferentsAuthorsSerializers(serializers.ModelSerializer):
    class Meta:      
        model = DifferentsAuthors
        fields = '__all__'
