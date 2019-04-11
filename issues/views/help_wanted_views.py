from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from issues.models.help_wanted_models import HelpWanted
from issues.serializers.help_wanted_serializers import HelpWantedSerializer
import requests

# Create your views here.

class HelpWantedView(APIView):
    def get(self,request,owner,repo):
        url = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues'
        help_wanted = HelpWanted.objects.all().filter(owner=owner, repo=repo)
        if(not help_wanted):
            issues = requests.get(url)
            issues = issues.json()

            for i in issues:
                id = i["id"]
                print(id)
            # HelpWanted.objects.create(
            #     total_issues = 
            #     help_wanted_issues = 
            # )
            
            return Response(issues)
        else:
            return Response('404')        
