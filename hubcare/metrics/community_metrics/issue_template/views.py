from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from issue_template.models import IssueTemplate
from issue_template.serializers import IssueTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.constants import URL_API


class IssueTemplateView(APIView):
    def get(self, request, owner, repo, token_auth):
        '''
        return if a repository issue template or not
        '''
        issue_template = IssueTemplate.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = IssueTemplateSerializer(issue_template)
        return Response(serializer.data)

    def post(self, request, owner, repo, token_auth):
        '''
        Post a new object
        '''
        issue_template = IssueTemplate.objects.filter(
            owner=owner,
            repo=repo
        )
        if issue_template:
            serializer = IssueTemplateSerializer(issue_template[0])
            return Response(serializer.data)

        github_status = get_github_request(owner, repo, token_auth)
        if github_status >= 200 and github_status < 300:
            response = create_issue_template(owner, repo, token_auth, True)
        elif github_status == 404:
            response = create_issue_template(owner, repo, token_auth, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)

    def put(self, request, owner, repo, token_auth):
        '''
        Update issue template object
        '''
        github_status = get_github_request(owner, repo, token_auth)
        if github_status >= 200 and github_status < 300:
            response = update_issue_template(owner, repo, token_auth, True)
        elif github_status == 404:
            response = update_issue_template(owner, repo, token_auth, False)
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(response)


def create_issue_template(owner, repo, token_auth, value):
    '''
    Create a new object in database
    '''
    issue_template = IssueTemplate.objects.create(
        owner=owner,
        repo=repo,
        issue_template=value,
    )
    serializer = IssueTemplateSerializer(issue_template)
    return serializer.data


def update_issue_template(owner, repo, token_auth, value):
    '''
    Update issue template object in database
    '''
    issue_template = IssueTemplate.objects.get(owner=owner, repo=repo)
    issue_template.issue_template = value
    issue_template.save()

    serializer = IssueTemplateSerializer(issue_template)
    return serializer.data


def get_github_request(owner, repo, token_auth):
    '''
    Request github repository data
    '''
    username = os.environ['NAME']
    token = os.environ['TOKEN']

    url = '{0}{1}/{2}/contents/.github/ISSUE_TEMPLATE'.format(
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
