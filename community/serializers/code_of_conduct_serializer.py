from rest_framework import serializers
from community.models.code_of_conduct_model import CodeOfConduct


class CodeOfConductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeOfConduct
        fields = '__all__'
