from rest_framework.views import APIView
from rest_framework.response import Response
from pull_request_template.models import PullRequestTemplate
from pull_request_template.serializers import PullRequestTemplateSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.functions import check_date, serialized_object
from community_metrics.constants import URL_API, HTTP_OK


class PullRequestTemplateView(APIView):
    def get(self, resquest, owner, repo, format=None):
        '''
        return if a repository have a pull request template or not
        '''
        pull_request_template = PullRequestTemplate.objects.all().filter(
            owner=owner,
            repo=repo
        )

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not pull_request_template):
            url = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = URL_API + owner + '/' + repo + url
            github_request = requests.get(result, auth=(username,
                                                        token))

            if(github_request.status_code == HTTP_OK):
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
            url = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = URL_API + owner + '/' + repo + url
            github_request = requests.get(result, auth=(username,
                                                        token))

            if(github_request.status_code == HTTP_OK):
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
        pull_request_template_serializer = serialized_object(
            PullRequestTemplateSerializer,
            pull_request_template
        )
        return Response(pull_request_template_serializer.data[0])
