from rest_framework import serializers
from readme.models import Readme


class ReadmeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Readme
        fields = '__all__'
