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
        contribution_guide = ContributionGuide.objects.all().filter(
            owner=owner,
            repo=repo
        )
        contribution_serialized = serialized_object(
            ContributionGuideSerializer,
            contribution_guide
        )
        return Response(contribution_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post a new object in database
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        url = '{0}{1}/{2}/contents/.github/CONTRIBUTING.md'.format(
            URL_API,
            owner,
            repo
        )
        github_request = requests.get(url, auth=(username, token))

        if(github_request.status_code == HTTP_OK):
            response = create_contribution_guide(owner, repo, True)
        else:
            response = create_contribution_guide(owner, repo, False)
        return Response(response)

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

        if(github_request.status_code == HTTP_OK):
            response = update_contribution_guide(owner, repo, True)
        else:
            response = update_contribution_guide(owner, repo, False)
        return Response(response)


def create_contribution_guide(owner, repo, value):
    '''
    Create a contribution guide object
    '''
    ContributionGuide.objects.create(
        owner=owner,
        repo=repo,
        contribution_guide=value,
        date_time=datetime.now(timezone.utc)
    )
    response = ContributionGuide.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        ContributionGuideSerializer,
        response
    ).data[0]


def update_contribution_guide(owner, repo, value):
    '''
    Update a contribution guide object
    '''
    ContributionGuide.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        contribution_guide=value,
        date_time=datetime.now(timezone.utc)
    )
    response = ContributionGuide.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        ContributionGuideSerializer,
        response
    ).data[0]
