from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from community.serializers.repository_description_serializer \
    import DescriptionSerializer
from community.models.repository_description_model import RepositoryDescription
import requests
from datetime import date


class ReadmeView(APIView):
    def get(self, request, owner, repo):

        description = RepositoryDescription.objects.all().filter(owner=owner, repo=repo)
        serialized = DescriptionSerializer(description, many=True)

        if (serialized.data == []):

            url = 'https://api.github.com/repos/'
            url2 = '/?/?'
            github_request = requests.get(url + owner + '/' + repo + url2)

            if(github_request.status_code == 200):
                DescriptionSerializer.objects.create(
                    owner=owner,
                    repo=repo,
                    description=True,
                    date=date.today()
                )
            else:
                DescriptionSerializer.objects.create(
                    owner=owner,
                    repo=repo,
                    description=False,
                    date=date.today()
                )

        description = RepositoryDescription.objects.all().filter(owner=owner, repo=repo)
        serialized = DescriptionSerializer(description, many=True)
        return Response(serialized.data)
