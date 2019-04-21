from rest_framework import serializers
from community.models.repository_description_model import RepositoryDescription


class DescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryDescription
        fields = '__all__'
