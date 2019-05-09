from rest_framework.views import APIView
from rest_framework.response import Response
from pull_request_template.models import PullRequestTemplate
from pull_request_template.serializers import PullRequestTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.function import check_date, filterObject


class PullRequestTemplateView(APIView):
    def get(self, resquest, owner, repo, format=None):
        '''
        return if a repository have a pull request template or not
        '''
        pull_request_template = filterObject(PullRequestTemplate)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not pull_request_template):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))

            if(github_request.status_code == 200):
                PullRequestTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    pull_request_template=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                PullRequestTemplate.objects.create(
                    owner=owner,
                    repo=repo,
                    pull_request_template=False,
                    date_time=datetime.now(timezone.utc)
                )

        elif(check_date(pull_request_template)):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))

            if(github_request.status_code == 200):
                PullRequestTemplate.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    pull_request_template=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                PullRequestTemplate.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    pull_request_template=False,
                    date_time=datetime.now(timezone.utc)
                )

        pull_request_template = PullRequestTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )
        pull_request_template_serializer = PullRequestTemplateSerializer(
            pull_request_template,
            many=True
        )
        return Response(pull_request_template_serializer.data[0])
