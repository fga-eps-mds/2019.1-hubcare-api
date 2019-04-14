from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from commits.models import Commit, CommitWeek
import requests
from datetime import date
from commits.serializers import CommitSerializer, CommitWeekSerializer


class CommitMonthView(APIView):

    def get(self, request, owner, repo):
        commit = Commit.objects.all().filter(owner=owner, repo=repo)
        serialized = CommitSerializer(commit, many=True)

        if (serialized.data != []):
            url = 'https://api.github.com/repos/'
            github_request = requests.get(url + owner + \
                                          '/' + repo + '/stats/participation')
            github_data = github_request.json()

            commit = Commit.objects.create(owner=owner,
                                           repo=repo,
                                           date=date.today()
                                           )

            week_number = 52
            for i in range(0, 52, 1):
                commit_week = CommitWeek.objects.create(week=week_number,
                                          quantity=github_data['all'][i], 
                                          commit=commit
                                          )
                week_number = week_number - 1

        commit = Commit.objects.all().filter(owner=owner, repo=repo)

        commits_week = CommitWeek.objects.all().filter(commit=commit.first())

        commits_week = CommitWeekSerializer(commits_week, many=True)

        sum = 0

        for i in range(-5, -1, 1):
            sum += commits_week.data[i]['quantity']

        data = {"owner": owner,
                "repo": repo,
                "sum": sum,
               }

        return Response(data)
