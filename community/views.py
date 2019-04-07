from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Readme
from .serializers import ReadmeSerializer
import requests

# Create your views here.
class ReadmeView(APIView):
    def get(self, request, owner, repo):
        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        readme_serialized = ReadmeSerializer(readme, many=True)
        if(readme_serialized.data == []):
            github_request = requests.get("https://api.github.com/repos/" + owner + "/" + repo + "/contents/README.md")
            print(github_request.json())
            if(github_request.status_code == 200):
                Readme.objects.create(owner=owner, repo=repo, has_readme=True)
            else:
                Readme.objects.create(owner=owner, repo=repo, has_readme=False)
        readme = Readme.objects.all().filter(owner=owner, repo=repo)
        readme_serialized = ReadmeSerializer(readme, many=True)
        return Response(readme_serialized.data)