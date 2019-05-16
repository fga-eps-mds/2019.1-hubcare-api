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


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo):
        activity_rate = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)[0]
        activity_rate_serialized = ActivityRateIssueSerializer(
            activity_rate)

        return Response(activity_rate_serialized.data)

    def post(self, request, owner, repo):
        activity_rate, activity_rate_15_days, activity_rate_15_days_metric = \
            self.get_activity_rate(owner, repo)

        data = {
            'owner': owner,
            'repo': repo,
            'activity_rate': activity_rate,
            'activity_rate_15_days': activity_rate_15_days,
            'activity_rate_15_days_metric': activity_rate_15_days_metric
        }

        serializer = ActivityRateIssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response('Error on create repository',
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner, repo):
        activity_rate_object = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)[0]

        activity_rate, activity_rate_15_days, activity_rate_15_days_metric = \
            self.get_activity_rate(owner, repo)

        data = {
            'activity_rate': activity_rate,
            'activity_rate_15_days': activity_rate_15_days,
            'activity_rate_15_days_metric': activity_rate_15_days_metric
        }

        serializer = ActivityRateIssueSerializer(activity_rate_object, data,
                                                 partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response('Error on updating repository',
                            status=status.HTTP_400_BAD_REQUEST)

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
        return activity_rate, activity_rate_15_days, metric


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
            print(activity)
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
        print(issues_alive)
        print(issues_not_alive)
        page_number = page_number + ONE
    return issues_alive, issues_not_alive
