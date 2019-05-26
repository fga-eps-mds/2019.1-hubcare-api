from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from contribution_guide.models import ContributionGuide
from contribution_guide.serializers import ContributionGuideSerializer
from datetime import date, datetime, timezone
import requests
import os
from community_metrics.constants import URL_API, HTTP_OK


class ContributionGuideView(APIView):
    def get(self, request, owner, repo):
        '''
        Return if a repository have a contribution guide
        or not
        '''
        contribution_guide = ContributionGuide.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = ContributionGuideSerializer(contribution_guide)
        return Response(serializer.data)

    def post(self, request, owner, repo):
        '''
        Post a new object in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        contribution_guide = ContributionGuide.objects.filter(
            owner=owner,
            repo=repo
        )
        if contribution_guide:
            serializer = ContributionGuideSerializer(contribution_guide[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = '{0}{1}/{2}/contents/.github/CONTRIBUTING.md'.format(
            URL_API,
            owner,
            repo
        )
        github_request = requests.get(url, auth=(username, token))
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = create_contribution_guide(owner, repo, True)
        elif status_code == 404:
            response = create_contribution_guide(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo):
        '''
        Update contribution guide object
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        url = '{0}{1}/{2}/contents/.github/CONTRIBUTING.md'.format(
            URL_API,
            owner,
            repo
        )
        github_request = requests.get(url, auth=(username, token))

        status_code = github_request.status_code
        if(status_code >= 200 and status_code < 300):
            response = update_contribution_guide(owner, repo, True)
        elif status_code == 404:
            response = update_contribution_guide(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_200_OK)


def create_contribution_guide(owner, repo, value):
    '''
    Create a contribution guide object
    '''
    contribution_guide = ContributionGuide.objects.create(
        owner=owner,
        repo=repo,
        contribution_guide=value,
    )
    serializer = ContributionGuideSerializer(contribution_guide)
    return serializer.data


def update_contribution_guide(owner, repo, value):
    '''
    Update a contribution guide object
    '''
    contribution_guide = ContributionGuide.objects.get(
        owner=owner,
        repo=repo
    )
    contribution_guide.contribution_guide = value
    contribution_guide.save()
    serializer = ContributionGuideSerializer(contribution_guide)
    return serializer.data
