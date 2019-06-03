from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from contributors.models import DifferentsAuthors
from contributors.serializers \
    import DifferentsAuthorsSerializers
from commit_metrics.constants import *
from datetime import datetime, timezone, timedelta
import requests
import os


class DifferentsAuthorsView(APIView):
    '''
        Get the number of different authors from a repo
        using GitHub Api of the
        last 14 days and return the total sum
        Input: owner, repo
        Output: Number of different authors in the last 14 days
        if the number is less than 4 if more than 4 and save data
    '''

    def get(self, request, owner, repo):
        '''
            Check the existence of the repo, if so get the number different
            authors of the last 14 days and save the data.
            Input: owner, repo
            Output: A list with the different authors o the last 14 days
            if the number is less than 4 if more than 4 and save data
        '''
        differents_authors = DifferentsAuthors.objects.all().filter(
            owner=owner,
            repo=repo
        )
        serializer = DifferentsAuthorsSerializers(differents_authors)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):

        differents_authors_object = DifferentsAuthors.objects.filter(
            owner=owner,
            repo=repo
        )

        if differents_authors_object:
            serializer = DifferentsAuthorsSerializers(
                differents_authors_object[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        differents_authors = self.get_contributors(owner, repo)

        differents_authors = DifferentsAuthors.objects.create(
            owner=owner,
            repo=repo,
            differents_authors=differents_authors
        )
        serializer = DifferentsAuthorsSerializers(differents_authors)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo):

        differents_authors = self.get_contributors(owner, repo)

        differents_authors_object = DifferentsAuthors.objects.get(
            owner=owner,
            repo=repo
        )
        differents_authors_object.differents_authors = differents_authors
        differents_authors_object.save()
        serializer = DifferentsAuthorsSerializers(differents_authors)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_contributors(self, owner, repo):
        username = os.environ['NAME']
        token = os.environ['TOKEN']
        github_request = requests.get(
            'https://api.github.com/repos/' + owner + '/' + repo + '/commits',
            auth=(username, token))
        github_data = github_request.json()
        present = datetime.today()
        days = timedelta(days=DAYS_CONTRIBUTORS)
        authorsCommits = []
        startTime = datetime.now()

        if (github_request.status_code >= 200 and
                github_request.status_code <= 299):

            for commit in github_data:
                commit['commit']['committer']['date'].split('T')[0]
                past = datetime.strptime(
                    commit['commit']['committer']['date'],
                    "%Y-%m-%dT%H:%M:%SZ")
                commitsDay = present - days
                if((past > commitsDay)):
                    authorsCommits.append(commit['commit']['author']['email'])
                    print(commit['commit']['author']['email'])
                    if(len(set(authorsCommits)) >= NUMBER_AUTHORS):
                        print(datetime.now() - startTime)
                        return len(set(authorsCommits))
        print(datetime.now() - startTime)

        return(len(set(authorsCommits)))
