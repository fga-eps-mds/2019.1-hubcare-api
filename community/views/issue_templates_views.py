from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.issue_templates_model import IssueTemplates
from community.serializers.issue_templates_serializer import IssueTemplatesSerializer
from datetime import datetime, timezone
import requests


class IssueTemplatesView(APIView):

    def get(self, request, owner, repo, format=None):
        issue_templates = IssueTemplates.objects.all().filter(owner=owner, repo=repo)

        if(not issue_templates): 
            issue_serialized = IssueTemplatesSerializer(issue_templates, many=True)
            url1 = 'https://api.github.com/repos/' 
            url2 = '/contents/.github/ISSUE_TEMPLATE.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result)
        
            if(github_request.status_code == 200):
                IssueTemplates.objects.create(
                    owner=owner, 
                    repo=repo, 
                    issue_templates=True, 
                    date=datetime.now(timezone.utc)
                )
            else:
                IssueTemplates.objects.create(owner=owner, 
                    repo=repo, 
                    issue_templates=False, 
                    date=datetime.now(timezone.utc)
                )
        elif(check_date(issue_templates)):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/ISSUE_TEMPLATE.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result)

            if(issue_templates.status_code == 200):
                IssueTemplates.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    pull_request_template=True,
                    date=datetime.now(timezone.utc)
                )
            else:
                IssueTemplates.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    pull_request_template=False,
                    date=datetime.now(timezone.utc)
                )

        issue_templates = IssueTemplates.objects.all().filter(owner=owner, repo=repo)
        issue_serializer = IssueTemplatesSerializer(issue_templates, many=True)
        return Response(issue_serialized.data[0])

def check_date(issue_templates):
    datetime_now = datetime.now(timezone.utc)
    if(issue_templates and (datetime_now - issue_templates[0].date).days >= 1):
        return True
    return False