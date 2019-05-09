from rest_framework.views import APIView
from rest_framework.response import Response
from code_of_conduct.models import CodeOfConduct
from code_of_conduct.serializers import CodeOfConductSerializer
from datetime import datetime, timezone
import requests
import os
from community_metrics.function import check_date, filterObject


class CodeOfConductView(APIView):
    def get(self, request, owner, repo):
        '''
        return if a repository has a code of conduct or not
        '''
        code_of_conduct = filterObject(CodeOfConduct)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if(not code_of_conduct):
            url1 = 'http://api.github.com/repos/'
            url2 = '/contents/.github/CODE_OF_CONDUCT.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == 200):
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo, code_of_conduct=False,
                    date_time=datetime.now(timezone.utc)
                )

        elif(check_date(code_of_conduct)):
            url1 = 'http://api.github.com/repos/'
            url2 = '/contents/.github/CODE_OF_CONDUCT.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result, auth=(username,
                                                        token))
            if(github_request.status_code == 200):
                CodeOfConduct.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=True,
                    date_time=datetime.now(timezone.utc)
                )
            else:
                CodeOfConduct.objects.filter(owner=owner, repo=repo).update(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=False,
                    date_time=datetime.now(timezone.utc)
                )

        code_of_conduct = CodeOfConduct.objects.all().filter(
            owner=owner,
            repo=repo
        )
        code_of_conduct_serialized = CodeOfConductSerializer(
            code_of_conduct,
            many=True
        )
        return Response(code_of_conduct_serialized.data[0])
