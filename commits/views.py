from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DifferentsAuthors 
from .serializers import DifferentsAuthorsSerializers
import requests

class DifferentsAuthorsView(APIView):

    def get(self, request, owner, repo):
        differentsauthors = DifferentsAuthors.objects.all().filter(owner=owner,repo=repo)
        differentsauthors_serialized = DifferentsAuthorsSerializers(differentsauthors, many = True)
        github_request = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/commits')
        return Response(github_request.json())