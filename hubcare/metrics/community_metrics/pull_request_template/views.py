from rest_framework.views import APIView
from rest_framework.response import Response
from pull_request_template.models import PullRequestTemplate
from pull_request_template.serializers import PullRequestTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.constants import URL_API, HTTP_OK


class PullRequestTemplateView(APIView):
    def get(self, request, owner, repo):
        '''
        Return if a repository have a pull request template or not
        '''
        pull_request_template = PullRequestTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )
        pull_request_template_serializer = serialized_object(
            PullRequestTemplateSerializer,
            pull_request_template
        )
        return Response(pull_request_template_serializer.data[0])

    def post(self, request, owner, repo):
        '''
        Post pull  request template object
        '''
        github_request = get_github_request(owner, repo)

        if(github_request.status_code == HTTP_OK):
            response = create_pull_request_template(owner, repo, True)
        else:
            response = create_pull_request_template(owner, repo, False)
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update pull request template object
        '''
        github_request = get_github_request(owner, repo)

        if(github_request.status_code == HTTP_OK):
            response = update_pull_request_template(owner, repo, True)
        else:
            response = update_pull_request_template(owner, repo, False)
        return Response(response)


def create_pull_request_template(owner, repo, value):
    '''
    Create pull request template object in database
    '''
    PullRequestTemplate.objects.create(
        owner=owner,
        repo=repo,
        pull_request_template=value,
        date_time=datetime.now(timezone.utc)
    )
    pull_request_template = PullRequestTemplate.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        PullRequestTemplateSerializer,
        pull_request_template
    ).data[0]


def update_pull_request_template(owner, repo, value):
    '''
    Update pull request template object in database
    '''
    PullRequestTemplate.objects.filter().update(
        owner=owner,
        repo=repo,
        pull_request_template=value,
        date_time=datetime.now(timezone.utc)
    )
    pull_request_template = PullRequestTemplate.objects.all().filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        PullRequestTemplateSerializer,
        pull_request_template
    ).data[0]


def get_github_request(owner, repo):
    '''
    Request Github data
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}/contents/.github/PULL_REQUEST_TEMPLATE.md'.format(
        URL_API,
        owner,
        repo
    )
    return requests.get(url, auth=(username, token))
