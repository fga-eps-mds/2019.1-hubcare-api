from rest_framework import serializers
from community.models.readme_model import Readme


class ReadmeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Readme
        fields = '__all__'
