from rest_framework.views import APIView
from rest_framework.response import Response
from issue_template.models import IssueTemplate
from issue_template.serializers import IssueTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions \
    import check_date, filter_object, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class IssueTemplateView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository have a readme or not
        '''
        issue_templates = filter_object(IssueTemplate)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not issue_templates):
            url = '/contents/.github/ISSUE_TEMPLATE'
            result = URL_API + owner + '/' + repo + url
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == HTTP_OK):
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
            url = '/contents/.github/ISSUE_TEMPLATE'
            result = URL_API + owner + '/' + repo + url
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == HTTP_OK):
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
        issue_serialized = serialized_object(
            IssueTemplateSerializer,
            issue_templates
            )
        return Response(issue_serialized.data[0])
