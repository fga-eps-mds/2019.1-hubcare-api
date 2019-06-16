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
    def get(self, request, owner, repo, token_auth):
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

    def post(self, request, owner, repo, token_auth):
        '''
        Post a new object in database
        '''
        contribution_guide = ContributionGuide.objects.filter(
            owner=owner,
            repo=repo
        )
        if contribution_guide:
            serializer = ContributionGuideSerializer(contribution_guide[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        github_status = get_github_request(owner, repo, token_auth)
        if github_status >= 200 and github_status < 300:
            response = create_contribution_guide(owner, repo, token_auth, True)
        elif github_status == 404:
            response = create_contribution_guide(owner, repo, token_auth, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)

    def put(self, request, owner, repo, token_auth):
        '''
        Update contribution guide object
        '''
        github_status = get_github_request(owner, repo, token_auth)
        if github_status >= 200 and github_status < 300:
            response = update_contribution_guide(owner, repo, token_auth, True)
        elif github_status == 404:
            response = update_contribution_guide(owner, repo, token_auth, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)


def create_contribution_guide(owner, repo, token_auth, value):
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


def update_contribution_guide(owner, repo, token_auth, value):
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


def get_github_request(owner, repo, token_auth):
    '''
    Request Github data
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}/contents/.github/CONTRIBUTING.md'.format(
        URL_API,
        owner,
        repo
    )
    request_status = requests.get(url, headers={'Authorization': 'token ' + token_auth}).status_code
    if request_status >= 200 and request_status < 300:
        return request_status
    elif request_status == 404:
        url = url.replace('.github/', '')
        request_status = requests.get(url, headers={'Authorization': 'token ' + token_auth}).status_code
    return request_status
