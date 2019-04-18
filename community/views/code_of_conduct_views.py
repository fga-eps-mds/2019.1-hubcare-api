from rest_framework.views import APIView
from rest_framework.response import Response
from community.models.code_of_conduct_model import CodeOfConduct
from community.serializers.code_of_conduct_serializer \
    import CodeofConductSerializer
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

        if(not code_of_conduct):
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

        elif(check_date(code_of_conduct)):
            url1 = 'http://api.github.com/repos/'
            url2 = '/contents/.github/CODE_OF_CONDUCT.md'
            result = url1 + owner + '/' + repo + url2
            github_request = requests.get(result)

            if(github_request.status_code == 200):
                CodeOfConduct.objects.filter().update(
                    owner=owner,
                    repo=repo,
                    code_of_conduct=True,
                    date=datetime.now(timezone.utc)
                )
            else:
                CodeOfConduct.objects.filter().update(
                    owner=owner,
                    repo=repo, code_of_conduct=False,
                    date=datetime.now(timezone.utc)
                )

        code_of_conduct = CodeOfConduct.objects.all().filter(
            owner=owner,
            repo=repo
        )
        code_serialized = CodeofConductSerializer(code_of_conduct, many=True)
        return Response(code_serialized.data[0])


def check_date(code_coonduct):
    '''
    verifies if the time difference between the last update and
    now is greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(code_coonduct and (datetime_now - code_coonduct[0].date).days >= 1):
        return True
    return False
