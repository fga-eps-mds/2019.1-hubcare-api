from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DifferentsAuthors 
from .serializers import DifferentsAuthorsSerializers
import requests
import datetime

class DifferentsAuthorsView(APIView):

    def get(self, request, owner, repo):
        differentsauthors = DifferentsAuthors.objects.all().filter(owner=owner,repo=repo)
        differentsauthors_serialized = DifferentsAuthorsSerializers(differentsauthors, many = True)
        github_request = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/commits')
        github_data = github_request.json()
        present = datetime.datetime.today()
        days = datetime.timedelta(days=30)
        commitsLastThirtyDays = []
        authorsCommits = []
        out = []

        for commit in github_data:
            commit['commit']['committer']['date'].split('T')[0]
            past = datetime.datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            commitsDay = present - days
            if((past > commitsDay)):
                commitsLastThirtyDays.append(commit['commit']['committer']['date'].split('T')[0])
                print(past.date())
                authorsCommits.append(commit['commit']['author']['name'])

       
        out.append(authorsCommits)
        out.append(commitsLastThirtyDays)
        return Response(out)