from rest_framework import status
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
        pull_request_template = PullRequestTemplate.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = PullRequestTemplateSerializer(pull_request_template)
        return Response(serializer.data)

    def post(self, request, owner, repo):
        '''
        Post pull  request template object
        '''
        pr_template = PullRequestTemplate.objects.filter(
            owner=owner,
            repo=repo
        )
        if pr_template:
            serializer = PullRequestTemplateSerializer(pr_template[0])
            return Response(serializer.data)

        github_request = get_github_request(owner, repo)
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = create_pull_request_template(owner, repo, True)
        elif status_code == 404:
            response = create_pull_request_template(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update pull request template object
        '''
        github_request = get_github_request(owner, repo)
        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            response = update_pull_request_template(owner, repo, True)
        elif status_code == 404:
            response = update_pull_request_template(owner, repo, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)


def create_pull_request_template(owner, repo, value):
    '''
    Create pull request template object in database
    '''
    pull_request_template = PullRequestTemplate.objects.create(
        owner=owner,
        repo=repo,
        pull_request_template=value,
    )
    serializer = PullRequestTemplateSerializer(pull_request_template)
    return serializer.data


def update_pull_request_template(owner, repo, value):
    '''
    Update pull request template object in database
    '''
    pull_request_template = PullRequestTemplate.objects.get(
        owner=owner,
        repo=repo
    )
    pull_request_template.pull_request_template = value
    pull_request_template.save()

    serializer = PullRequestTemplateSerializer(pull_request_template)
    return serializer.data


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
