from rest_framework import serializers
from release_note.models import ReleaseNote


class ReleaseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseNote
        fields = [
            'release_note'
        ]
