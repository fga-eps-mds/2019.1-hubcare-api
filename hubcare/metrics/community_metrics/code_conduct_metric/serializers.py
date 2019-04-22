from rest_framework import serializers
from code_conduct_metric.models import CodeOfConduct


class CodeOfConductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeOfConduct
        fields = '__all__'
