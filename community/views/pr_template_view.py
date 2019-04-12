from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.pr_template_model import Community
from community.serializers.pr_template_serializer import CommunitySerializer
from datetime import date
import requests


class PullRequestTemplateView(APIView):
    def get(self, resquest, owner, repo, format=None):
        community = Community.objects.all().filter(owner=owner, repo=repo)
        community_serializer = CommunitySerializer(community, many=True)

        if(community_serializer.data == []):
            url1 = 'https://api.github.com/repos/'
            url2 = '/contents/.github/PULL_REQUEST_TEMPLATE.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result)

            if(github_request.status_code == 200):
                Community.objects.create(owner=owner,
                                         repo=repo,
                                         pull_request_template=True,
                                         date=date.today())
            else:
                Community.objects.create(owner=owner,
                                         repo=repo,
                                         pull_request_template=False,
                                         date=date.today())

        community = Community.objects.all().filter(owner=owner, repo=repo)
        community_serializer = CommunitySerializer(community, many=True)
        return Response(community_serializer.data[0])
