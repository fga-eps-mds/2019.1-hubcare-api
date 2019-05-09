from rest_framework.views import APIView
from rest_framework.response import Response
from issue_template.models import IssueTemplate
from issue_template.serializers import IssueTemplateSerializer
from datetime import date, datetime, timezone
import requests
import os


class IssueTemplateView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a readme or not
        '''
        issue_templates = IssueTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not issue_templates):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/ISSUE_TEMPLATE'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == 200):
                IssueTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    issue_templates=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                IssueTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    issue_templates=False,
                    date_time=datetime.now(timezone.utc)
                )
        elif(check_date(issue_templates)):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/ISSUE_TEMPLATE'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == 200):
                IssueTemplate.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    issue_templates=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                IssueTemplate.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    issue_templates=False,
                    date_time=datetime.now(timezone.utc)
                )

        issue_templates = IssueTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )
        issue_serialized = IssueTemplateSerializer(issue_templates, many=True)
        return Response(issue_serialized.data[0])


def check_date(issue):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(issue and (datetime_now - issue[0].date_time).days >= 1):
        return True
    return False
