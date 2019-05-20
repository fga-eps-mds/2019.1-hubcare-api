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
        Input: owner, repo
        Output: the sum of commits
    '''
    def get(self, request, owner, repo):
        '''
            Input: owner, repo
            Output: the sum of commits
        '''

        commit = CommitMonth.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = CommitMonthSerializer(commit)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):
        
        commit = CommitMonth.objects.filter(
            owner=owner,
            repo=repo
        )

        if commit:
            serializer = CommitMonthSerializer(commit, many=True)
            return Response(serializer.data[0], status=status.HTTP_200_OK)

        commits_week, total_commits = self.get_commits_by_week(owner, repo)

        commit = CommitMonth.objects.create(
            owner=owner,
            repo=repo,
            commits_week=commits_week,
            total_commits=total_commits
        )
        serializer = CommitMonthSerializer(commit)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo):

        commits_week, total_commits = self.get_commits_by_week(owner, repo)

        commit_month = CommitMonth.objects.update(
            commits_week=commits_week,
            total_commits=total_commits
        )        
        commit_month_object = CommitMonth.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = CommitMonthSerializer(commit_month_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_commits_by_week(self, owner, repo):
        '''
        Returns an array with the number of commits per week in the last 4
        weeks and the total sum of commits in this period
        '''

        username = os.environ['NAME']
        token = os.environ['TOKEN']

        github_request = requests.get(
            MAIN_URL + owner + '/' + repo + WEEKLY_COMMITS,
            auth=(username, token)
        ).json()

        commits_week_array = github_request['all'][FIRST_WEEK:LAST_WEEK]
        total_commits = 0
        for i in commits_week_array:
            total_commits += i

        commits_week = json.dumps(commits_week_array)

        return commits_week, total_commits
