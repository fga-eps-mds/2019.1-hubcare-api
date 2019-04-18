from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.serializers import ReadmeSerializer
from community.models.readme_model import Readme
import requests
from datetime import date


class ReadmeView(APIView):
    def get(self, request, owner, repo):

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)

        if (serialized.data == []):

            url = 'https://api.github.com/repos/'
            url2 = '/contents/README.md'
            github_request = requests.get(url + owner + '/' + repo + url2)

            if(github_request.status_code == 200):
                Readme.objects.create(
                    owner=owner,
                    repo=repo,
                    readme=True,
                    date=date.today()
                )
            else:
                Readme.objects.create(
                    owner=owner,
                    repo=repo,
                    readme=False,
                    date=date.today()
                )

        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        serialized = ReadmeSerializer(readme, many=True)
        return Response(serialized.data)
