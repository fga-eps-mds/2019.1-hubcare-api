from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.issue_templates_model import IssueTemplates
from community.serializers.issue_templates_serializer import IssueTemplatesSerializer


class IssueTemplatesView(APIView):

    def get(self, resquest, owner, repo, format=None):
        issue_templates = IssueTemplates.Objects.all().filter(owner=owner, repo=repo)

        if(not issue_templates):
            url1 = 'https://api.github.com/repos/' 
            url2 = '/contents/.github/ISSUE_TEMPLATE'
            result = url1 + owner + '/' + repo + url2
            github_request = resquests.get(result)

            if(github_request.status_code == 200):
                IssueTemplates.objects.create(owner=owner, repo=repo, issue_templates=True, date=date.now(timezone.utc))
