from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PullRequestTemplateSerializer
from .models import PullRequestTemplate
import requests

class PullRequestTemplateView(APIView):

    def get(self, requests):

        result = requests.get('https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api')
        result = result.json()

        PullRequestTemplate =  PullRequestTemplate.objects.all()
        serializer = PullRequestTemplateSerializer(PullRequestTemplate, many=True)

        return Response(result['pulls_url'])
