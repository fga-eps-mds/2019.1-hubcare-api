from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from commit_month.models import CommitMonth
from commit_month.serializers import CommitMonthSerializer
from datetime import datetime, timezone, timedelta
from commit_metrics.constants import *
import requests
import json
import os


class CommitMonthView(APIView):
    '''
        Get commits of the last month from GitHub Api and return the total sum
        Input: owner, repo, token_auth
        Output: the sum of commits
    '''
    def get(self, request, owner, repo, token_auth):
        '''
            Input: owner, repo, token_auth
            Output: the sum of commits
        '''

        commit = CommitMonth.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = CommitMonthSerializer(commit)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo, token_auth):

        commit = CommitMonth.objects.filter(
            owner=owner,
            repo=repo
        )

        if commit:
            serializer = CommitMonthSerializer(commit[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        commits_week, total_commits, commits_last_period = \
            self.get_commits_by_week(owner, repo, token_auth)

        commit = CommitMonth.objects.create(
            owner=owner,
            repo=repo,
            commits_week=commits_week,
            commits_last_period=commits_last_period,
            commits_high_score=COMMITS_HIGH_SCORE,
            total_commits=total_commits
        )
        serializer = CommitMonthSerializer(commit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo, token_auth):

        commits_week, total_commits, commits_last_period = \
            self.get_commits_by_week(owner, repo, token_auth)

        commit_month_object = CommitMonth.objects.get(
            owner=owner,
            repo=repo
        )
        commit_month_object.commits_week = commits_week
        commit_month_object.total_commits = total_commits
        commit_month_object.commits_high_score = COMMITS_HIGH_SCORE
        commit_month_object.commits_last_period = commits_last_period
        commit_month_object.save()
        serializer = CommitMonthSerializer(commit_month_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_commits_by_week(self, owner, repo, token_auth):
        '''
        Returns an array with the number of commits per week in the last 4
        weeks and the total sum of commits in this period
        '''

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        github_request = requests.get(
            MAIN_URL + owner + '/' + repo + WEEKLY_COMMITS,
            headers={'Authorization': 'token ' + token_auth}
        )

        status_code = github_request.status_code
        if status_code >= 200 and status_code < 300:
            github_request = github_request.json()
            commits_week_array = github_request['all'][FIRST_WEEK:LAST_WEEK]
            commits_last_period = sum(commits_week_array[-PERIOD:])
            total_commits = 0
            for i in commits_week_array:
                total_commits += i

            commits_week = json.dumps(commits_week_array)

            return commits_week, total_commits, commits_last_period
        else:
            return Response('Error on requesting GitHubAPI',
                            status=status.HTTP_400_BAD_REQUEST)
