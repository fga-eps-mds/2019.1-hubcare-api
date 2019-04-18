from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.code_of_conduct_model import CodeOfConduct
from community.serializers.code_of_conduct_serializer \
    import CodeOfConductSerializer
from datetime import datetime, timezone
import requests


class CodeOfConductView(APIView):

    def get(self, request, owner, repo):
        '''
        return if a repository has a code of conduct or not
        '''
        code_of_conduct = CodeOfConduct.objects.all().filter(
            owner=owner,
            repo=repo
        )

        if(not code_of_conduct.exists()):
            url1 = 'http://api.github.com/repos/'
            url2 = '/contents/.github/CODE_OF_CONDUCT.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result)
            if(github_request.status_code == 200):
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=True,
                    date=datetime.now(timezone.utc)
                )
            else:
                CodeOfConduct.objects.create(
                    owner=owner,
                    repo=repo, code_of_conduct=False,
                    date=datetime.now(timezone.utc)
                )
        else:
            list_code_of_conduct = list(code_of_conduct)
            if(check_date(list_code_of_conduct[-1])):
                url1 = 'http://api.github.com/repos/'
                url2 = '/contents/.github/CODE_OF_CONDUCT.md'
                result = url1 + owner + '/' + repo + url2
                github_request = requests.get(result)
                if(github_request.status_code == 200):
                    CodeOfConduct.objects.create(
                        owner=owner,
                        repo=repo,
                        code_of_conduct=True,
                        date=datetime.now(timezone.utc)
                    )
                else:
                    CodeOfConduct.objects.create(
                        owner=owner,
                        repo=repo, code_of_conduct=False,
                        date=datetime.now(timezone.utc)
                    )
            else:
                code_of_conduct = CodeOfConduct.objects.all().filter(
                    owner=owner,
                    repo=repo
                )

        code_serialized = CodeOfConductSerializer(code_of_conduct, many=True)
        return Response(code_serialized.data[-1])


def check_date(code_of_conduct):
    datetime_now = datetime.now(timezone.utc)
    if(code_of_conduct and (datetime_now - code_of_conduct.date).days >= 1):
        return True
    return False
