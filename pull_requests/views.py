from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PullRequestTemplateSerializer
from .models import PullRequestTemplate
import requests

class PullRequestTemplateView(APIView):

    def get(self, request):

        result = requests.get('https://api.github.com/repos/fga-eps-mds/2019.1-hubcare-api/contents/.github/PULL_REQUEST_TEMPLATE.md?ref=master')
        result = result.json()

        pull_requests =  PullRequestTemplate.objects.all()
        serializer = PullRequestTemplateSerializer(pull_requests, many=True)

        return Response(result['url'])