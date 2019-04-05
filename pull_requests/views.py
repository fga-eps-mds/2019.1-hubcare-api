from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PullRequestTemplateSerializer
from .models import PullRequestTemplate
import requests

class PullRequestTemplateView(APIView):

    def get(self, request, owner, repo):

        url1 = 'https://api.github.com/repos/'
        url2 = '/contents/.github/PULL_REQUEST_TEMPLATE.md?ref=master'
        result = requests.get(url1 + owner + '/' + repo + url2)
        result = result.json()

        try:
            if(result['html_url']) != None:
                return Response(True)
            else:
                return Response(False)
        except:
            raise Http404