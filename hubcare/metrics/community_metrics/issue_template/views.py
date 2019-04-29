from rest_framework.views import APIView
from rest_framework.response import Response
from issue_template.models import IssueTemplate
from issue_template.serializers import IssueTemplateSerializer
from datetime import date
import requests
import os


class IssueTemplateView(APIView):

    def get(self, request, owner, repo):
        issue_templates = IssueTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )


        if(not issue_templates):

            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/ISSUE_TEMPLATE'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(os.environ['USERNAME'], os.environ['TOKEN']))
            if(github_request.status_code == 200):
                IssueTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    issue_templates=True,
                    date=date.today()
                )
            else:
                IssueTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    issue_templates=False,
                    date=date.today()
                )

        issue_templates = IssueTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )
        issue_serialized = IssueTemplateSerializer(issue_templates, many=True)
        return Response(issue_serialized.data[0])
