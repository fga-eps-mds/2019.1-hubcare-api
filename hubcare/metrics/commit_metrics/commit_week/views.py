from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from commit_metrics.models import Commit
from commit_week.models import CommitWeek
from commit_metrics.serializers import CommitSerializer
from commit_week.serializers import CommitWeekSerializer
from datetime import datetime, timezone, timedelta
from commit_metrics.constants import *
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
        # commit = Commit.objects.all().filter(owner=owner, repo=repo)
        # serialized = CommitSerializer(commit, many=True)

        data = Commit.objects.all()
        serializer = CommitSerializer(data, many=True)
 
        return Response(serializer.data) # REMOVER

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        month = timedelta(days=30)
        date_now = datetime.now()
        last_month = str(date_now - month).replace(' ','-')

        url_since = '/commits?since='
        url_page = '&per_page=100&page='
        page = 1
        commits_month = []
        while True:
            commits_month_request = requests.get(
                MAIN_URL + owner + '/' + repo +
                url_since + last_month +
                url_page + str(page),
                auth=(username, token)
            ).json()

            if commits_month_request:
                commits_month += commits_month_request
                page += 1
            else:
                break

        count = 0
        for i in commits_month:
            count += 1
        print(count)

        return Response('ok')
        # try:
        #     commits_week = CommitWeek.objects.filter(
        #         owner=owner,
        #         repo=repo
        #     )
            
        #     serializer = CommitWeekSerializer(commits_week, many=True)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # except:
        #     return Response('There is no repository for this metric',
        #                     status=status.HTTP_400_BAD_REQUEST)

        ###################################################################
        # url2 = '/stats/participation'
        # github_request = requests.get(MAIN_URL + owner + '/' + repo + url2,
        #                                 auth=(username, token))

        # github_data = github_request.json()

        # commit = Commit.objects.create(
        #     owner=owner,
        #     repo=repo,
        # )
        # week_number = YEAR_WEEK
        # for i in range(0, YEAR_WEEK, 1):
        #     if len(github_data['all']) >= 1:
        #         commit_week = CommitWeek.objects.create(
        #             week=week_number,
        #             quantity=github_data['all'][i],
        #             commit=commit
        #         )
        #     week_number = week_number - 1

        # commit = Commit.objects.all().filter(owner=owner, repo=repo)

        # commits_week = CommitWeek.objects.all().filter(commit=commit.first())

        # commits_week = CommitWeekSerializer(commits_week, many=True)

        # sum = 0

        # if commits_week.data:
        #     for i in range(FIRST_WEEK, LAST_WEEK, 1):
        #         sum += commits_week.data[i]['quantity']

        # data = {
        #     "owner": owner,
        #     "repo": repo,
        #     "sum": sum,
        # }

        # return Response(data)

    def post(self, request, owner, repo):

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        commit = Commit.objects.create(
            owner=owner,
            repo=repo
        )

        github_request = requests.get(
            MAIN_URL + owner + '/' + repo + WEEKLY_COMMITS,
            auth=(username, token)
        ).json()

        commits_week_array = github_request['all'][FIRST_WEEK:LAST_WEEK]

        total_quantity = 0
        week = 1
        for i in commits_week_array:
            total_quantity += i
            commit_week = CommitWeek.objects.create(
                week = week,
                quantity = i,
                commit = commit
            )
            week += 1

        commits_week = CommitWeek.objects.filter(
            commit__owner=owner,
            commit__repo=repo
        )
        serializer = CommitWeekSerializer(commits_week, many=True)

        return Response(serializer.data)