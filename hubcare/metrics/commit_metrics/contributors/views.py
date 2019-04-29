from rest_framework.views import APIView
from rest_framework.response import Response
from contributors.models import DifferentsAuthors
from contributors.serializers \
    import DifferentsAuthorsSerializers
import requests
import datetime
import os


class DifferentsAuthorsView(APIView):

    def get(self, request, owner, repo):
        differentsauthors = DifferentsAuthors.objects.all().filter(
            owner=owner,
            repo=repo
        )
        differentsauthors_serialized = DifferentsAuthorsSerializers(
            differentsauthors,
            many=True)
        username = os.environ['NAME']
        token = os.environ['TOKEN']
        github_request = requests.get(
            'https://api.github.com/repos/' + owner + '/' + repo + '/commits',
            auth=(username, token))
        github_data = github_request.json()
        present = datetime.datetime.today()
        days = datetime.timedelta(days=30)
        commitsLastThirtyDays = []
        authorsCommits = []
        out = []
        listCommits = []
        listJson = []

        for commit in github_data:
            commit['commit']['committer']['date'].split('T')[0]
            past = datetime.datetime.strptime(
                commit['commit']['committer']['date'],
                "%Y-%m-%dT%H:%M:%SZ")
            commitsDay = present - days
            if((past > commitsDay)):
                commitsLastThirtyDays.append(
                    commit['commit']['committer']['date'].split('T')[0])
                authorsCommits.append(commit['commit']['author']['email'])
        authorsDistintCommits = set(authorsCommits)
        for author in authorsDistintCommits:
            listJson.append({'author': author,
                             'numberCommits': authorsCommits.count(author)})
        return Response(listJson)
