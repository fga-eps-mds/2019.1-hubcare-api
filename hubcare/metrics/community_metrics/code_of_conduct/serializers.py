from rest_framework import serializers
from code_of_conduct.models import CodeOfConduct


class CodeOfConductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeOfConduct
        fields = '__all__'
