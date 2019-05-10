from rest_framework.views import APIView
from rest_framework.response import Response
from commit_metrics.models import Commit
from commit_week.models import CommitWeek
from commit_metrics.serializers import CommitSerializer
from commit_week.serializers import CommitWeekSerializer
from datetime import date
from commit_week.constants import *
from django.http import Http404
import requests
import os


class CommitMonthView(APIView):
    '''
        Get commits of the last month from GitHub Api and return the total sum
        Input: owner, repo
        Output: the sum of commits
    '''
    def get(self, request, owner, repo):
        '''
            Check the existence of the repo, if so get the number of commits
            for each week in the last year and filter the last four weeks.
            Input: owner, repo
            Output: the sum of commits
        '''
        commit = Commit.objects.all().filter(owner=owner, repo=repo)
        serialized = CommitSerializer(commit, many=True)

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        if (not commit):
            url = 'https://api.github.com/repos/'
            url2 = '/stats/participation'
            github_request = requests.get(url + owner + '/' + repo + url2,
                                          auth=(username, token))

            github_data = github_request.json()

            if(github_request.status_code == STATUS_ERROR):
                raise Http404

            else:
                commit = Commit.objects.create(
                    owner=owner,
                    repo=repo,
                    date=date.today()
                )
                week_number=YEAR_WEEK
                for i in range(0, YEAR_WEEK, 1):
                    if len(github_data['all']) >= 1:
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

        if commits_week.data:
            for i in range(FIRST_WEEK, LAST_WEEK, 1):
                sum += commits_week.data[i]['quantity']

        data = {"owner": owner,
                "repo": repo,
                "sum": sum,
        }

        return Response(data)
