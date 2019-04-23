from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import * 


class SupportQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo)


        if(github_request.status_code == 200):
            url = URL_COMMMUNITY + 'readme/' + owner + '/' + repo
            readme_metric = requests.get(url)
            print(readme_metric.json())
            url = URL_COMMMUNITY + 'issue_template/' + owner + '/' + repo
            issue_template_metric = requests.get(url)
            print(issue_template_metric.json())
        
        return Response("ok")




