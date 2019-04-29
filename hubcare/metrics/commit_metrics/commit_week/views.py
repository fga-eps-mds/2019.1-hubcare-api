from rest_framework.views import APIView
from rest_framework.response import Response
from commit_metrics.models import Commit
from commit_week.models import CommitWeek
from commit_metrics.serializers import CommitSerializer
from commit_week.serializers import CommitWeekSerializer
from datetime import date
import requests
import os


class CommitMonthView(APIView):

    def get(self, request, owner, repo):
        commit = Commit.objects.all().filter(owner=owner, repo=repo)
        serialized = CommitSerializer(commit, many=True)

        if (serialized.data != []):
            url = 'https://api.github.com/repos/'
            url2 = '/stats/participation'
            github_request = requests.get(url + owner + '/' + repo + url2,
                                          auth=(os.environ['USERNAME'],
                                          os.environ['TOKEN']))
            github_data = github_request.json()

            commit = Commit.objects.create(
                owner=owner,
                repo=repo,
                date=date.today()
            )

            week_number = 52
            for i in range(0, 52, 1):
                commit_week = CommitWeek.objects.create(
                    week=week_number,
                    quantity=github_data['all'][i],
                    commit=commit
                )
                week_number = week_number - 1

        commit = Commit.objects.all().filter(owner=owner, repo=repo)

        commits_week = CommitWeek.objects.all().filter(commit=commit.first())

        commits_week = CommitWeekSerializer(commits_week, many=True)

        sum = 0

        # for i in range(-5, -1, 1):
        #     sum += commits_week.data[i]['quantity']

        data = {"owner": owner,
                "repo": repo,
                "sum": sum,
                }

        return Response(data)
        # return Response('ok')
