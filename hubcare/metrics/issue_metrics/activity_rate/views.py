import requests
import re
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from activity_rate.models import ActivityRateIssue
from activity_rate.serializers import ActivityRateIssueSerializer
from issue_metrics.functions import calculate_metric, \
        get_all_issues, check_datetime_15_days
from issue_metrics.constants import ONE, ZERO
import os

from datetime import datetime, timezone


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        Return activity rate to repo issues
        '''
        activity_rate = ActivityRateIssue.objects.get(
            owner=owner,
            repo=repo
        )
        activity_rate_serialized = ActivityRateIssueSerializer(
            activity_rate
        )

        return Response(
            activity_rate_serialized.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, owner, repo):
        '''
        Create new activity rate object
        '''
        data = ActivityRateIssue.objects.filter(
            owner=owner,
            repo=repo
        )
        if data:
            serializer = ActivityRateIssueSerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        activity_rate, activity_rate_15_days, activity_rate_15_days_metric, \
            active_issues, dead_issues = self.get_activity_rate(owner, repo)

        data = ActivityRateIssue.objects.create(
            owner=owner,
            repo=repo,
            activity_rate=float("{0:.2f}".format(activity_rate)),
            activity_rate_15_days=float("{0:.2f}".format(
                activity_rate_15_days
            )),
            activity_rate_15_days_metric=float("{0:.2f}".format(
                activity_rate_15_days_metric
            )),
            active_issues=active_issues,
            dead_issues=dead_issues
        )

        serializer = ActivityRateIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, owner, repo):
        activity_rate_object = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)[0]

        activity_rate, activity_rate_15_days, activity_rate_15_days_metric, \
            active_issues, dead_issues = self.get_activity_rate(owner, repo)

        data = ActivityRateIssue.objects.get(
            owner=owner,
            repo=repo
        )
        data.activity_rate = float("{0:.2f}".format(activity_rate))
        data.activity_rate_15_days = float("{0:.2f}".format(
                activity_rate_15_days
            ))
        data.activity_rate_15_days_metric = float("{0:.2f}".format(
                activity_rate_15_days_metric
            ))
        data.active_issues = active_issues
        data.dead_issues = dead_issues
        data.save()

        serializer = ActivityRateIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_activity_rate(self, owner, repo):
        open_issues, closed_issues = get_all_issues(owner, repo)
        issues_alive, not_alive = get_issues_15_day(owner, repo)
        if(not_alive != ZERO):
            activity_rate_15_days = issues_alive / not_alive
        else:
            activity_rate_15_days = ZERO

        if (closed_issues + open_issues) == 0:
            activity_rate = 0
        else:
            activity_rate = open_issues / (closed_issues + open_issues)

        metric = calculate_metric(issues_alive, not_alive)
        dead_issues = not_alive - issues_alive
        return activity_rate, activity_rate_15_days, metric, issues_alive, \
            dead_issues


def get_issues_15_day(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    page_number = ONE
    issues_alive = ZERO
    issues_not_alive = ZERO
    u = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues?&page='
    aux = True

    username = os.environ['NAME']
    token = os.environ['TOKEN']

    while aux:
        github_request = requests.get(u + str(page_number) + '&per_page=100',
                                      auth=(username, token))
        github_data = github_request.json()

        for activity in github_data:
            if(check_datetime_15_days(activity['updated_at'])):
                if(activity['state'] == 'open'):
                    issues_alive = issues_alive + ONE
                else:
                    # Do nothing
                    pass
            if(activity['state'] == 'open'):
                issues_not_alive = issues_not_alive + ONE
            else:
                # Do nothing
                pass

        if(github_data == []):
            aux = False
        page_number = page_number + ONE
    return issues_alive, issues_not_alive
