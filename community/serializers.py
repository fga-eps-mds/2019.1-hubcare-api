from rest_framework import serializers
from .models import Readme

class ReadmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Readme
        fields = '__all__'
