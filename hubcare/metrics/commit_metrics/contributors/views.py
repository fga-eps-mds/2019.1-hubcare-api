from rest_framework.views import APIView
from rest_framework.response import Response
from contributors.models import DifferentsAuthors
from contributors.serializers \
    import DifferentsAuthorsSerializers
from contributors.constants import *
import requests
import datetime
import os


class DifferentsAuthorsView(APIView):
    '''
        Get the number of different authors from a repo using GitHub Api of the
        last 30 days and return the total sum
        Input: owner, repo
        Output: A list with the different authors o the last 30 days
        and save data
    '''
    def get(self, request, owner, repo):
        '''
            Check the existence of the repo, if so get the number different
            authors of the last 30 days and save the data.
            Input: owner, repo
            Output: A list with the different authors o the last 30 days
            and save data
        '''
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
        days = datetime.timedelta(days=month_days)
        commitsLastThirtyDays = []
        authorsCommits = []
        out = []
        listCommits = []
        listJson = []

        if (github_request.status_code >= status_ok and
                github_request.status_code <= status_no_content):

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
