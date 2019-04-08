from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PullRequestTemplateSerializer
from .models import PullRequestTemplate
from datetime import date
import requests

class PullRequestTemplateView(APIView):

    def get(self, request, owner, repo):
        pull_request_template = PullRequestTemplate.objects.all().filter(owner=owner, repo=repo)
        pull_request_template_serializer = PullRequestTemplateSerializer(pull_request_template, many=True)
        
        if (pull_request_template_serializer.data == []):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = requests.get(url1 + owner + '/' + repo + url2)
            print(result.json())

            if(result.status_code == 200):
                PullRequestTemplate.objects.create(owner=owner, repo=repo, has_pull_request_template=True, date=date.today())
            else:
                PullRequestTemplate.objects.create(owner=owner, repo=repo, has_pull_request_template=False, date=date.today())

        pull_request_template = PullRequestTemplate.objects.all().filter(owner=owner, repo=repo)
        pull_request_template_serialized = PullRequestTemplateSerializer(pull_request_template, many=True)
        return Response(pull_request_template_serialized.data)