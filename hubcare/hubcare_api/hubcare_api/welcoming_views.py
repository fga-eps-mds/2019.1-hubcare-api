from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import * 


class WelcomingQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request =  requests.get(url + owner + '/' + repo)

        if(github_request.status_code == 200):
            url = URL_COMMIT + 'contributors/different_authors/' + owner + '/' + repo
            contributors_metric = requests.get(url)
            print(contributors_metric.json())
        
        return Response('ok')