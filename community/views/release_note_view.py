from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.release_note_models \
    import ReleaseNoteCheck
from community.serializers.release_note_serializers \
    import ReleaseNoteCheckSerializers
from datetime import datetime
import requests


class ReleaseNoteCheckView(APIView):

    def get(self, request, owner, repo):
        realeasenotecheck = ReleaseNoteCheck.objects.all().filter(
            owner=owner,
            repo=repo
        )
        realeasenotecheck_serialized = ReleaseNoteCheckSerializers(
            realeasenotecheck,
            many=True
        )
        github_request = requests.get(
            'https://api.github.com/repos/' + owner + '/' + repo + '/releases'
        )
        github_data = github_request.json()

        return Response(github_request.json())
