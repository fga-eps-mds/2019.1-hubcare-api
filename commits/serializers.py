from rest_framework import serializers
from .models import DifferentsAuthors


class DifferentsAuthorsSerializers(serializers.ModelSerializer):
    class Meta:
        
        model = DifferentsAuthors
        fields = '__all__'