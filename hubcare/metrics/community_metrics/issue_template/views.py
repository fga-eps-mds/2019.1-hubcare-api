from rest_framework.views import APIView
from rest_framework.response import Response
from issue_template.models import IssueTemplate
from issue_template.serializers import IssueTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class IssueTemplateView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a readme or not
        '''
        issue_templates = IssueTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )
        issue_serialized = serialized_object(
            IssueTemplateSerializer,
            issue_templates
            )
        return Response(issue_serialized.data[0])

    def post(self, request, owner, repo):
        '''
        Post a new object
        '''
        github_request = get_github_request(owner, repo)
        if(github_request.status_code == HTTP_OK):
            response = create_issue_template(owner, repo, True)
        else:
            response = create_issue_template(owner, repo, False)
        return Response(response)

    def put(self, request, owner, repo):
        '''
        Update issue template object
        '''
        github_request = get_github_request(owner, repo)

        if(github_request.status_code == HTTP_OK):
            response = update_issue_template(owner, repo, True)
        else:
            response = update_issue_template(owner, repo, False)
        return Response(response)


def create_issue_template(owner, repo, value):
    '''
    Create a new object in database
    '''
    IssueTemplate.objects.create(
        owner=owner,
        repo=repo,
        issue_templates=value,
        date_time=datetime.now(timezone.utc)
    )
    issue_template = IssueTemplate.objects.filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        IssueTemplateSerializer,
        issue_template
    ).data[0]


def update_issue_template(owner, repo, value):
    '''
    Update issue template object in database
    '''
    IssueTemplate.objects.filter(owner=owner, repo=repo).update(
        owner=owner,
        repo=repo,
        issue_templates=value,
        date_time=datetime.now(timezone.utc)
    )
    issue_template = IssueTemplate.objects.filter(
        owner=owner,
        repo=repo
    )
    return serialized_object(
        IssueTemplateSerializer,
        issue_template
    ).data[0]


def get_github_request(owner, repo):
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
    return requests.get(url, auth=(username, token))
