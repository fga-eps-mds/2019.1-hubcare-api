from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.code_of_conduct_model import CodeOfConduct
from community.serializers.code_of_conduct_serializer \
    import CodeofConductSerializer
from datetime import date
import requests


class CodeOfConductView(APIView):

    def get(self, request, owner, repo):
        code_of_conduct = CodeOfConduct.objects.all().filter(
            owner=owner,
            repo=repo
        )
        code_serialized = CodeofConductSerializer(code_of_conduct, many=True)

        if(code_serialized.data == []):

            url1 = 'http://api.github.com/repos/'
            url2 = '/contents/.github/CODE_OF_CONDUCT.md'
            github_request = requests.get(url1 + owner + '/' + repo + url2)

            if(github_request.status_code == 200):
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=True,
                    date=date.today()
                )
            else:
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo, code_of_conduct=False,
                    date=date.today()
                )

        code_of_conduct = CodeOfConduct.objects.all().filter(
            owner=owner,
            repo=repo
        )
        code_serialized = CodeofConductSerializer(code_of_conduct, many=True)
        return Response(code_serialized.data)
