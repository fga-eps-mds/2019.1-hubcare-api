from rest_framework import serializers
from release_note.models import ReleaseNoteCheck


class ReleaseNoteCheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReleaseNoteCheck
        fields = '__all__'
