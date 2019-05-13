import requests
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ActivityRateIssue
from .serializers import ActivityRateIssueSerializers
from issue_metrics.functions import check_datetime, \
    calculate_metric, get_all_issues, check_datetime_15_days
from issue_metrics.constants import ZERO
from datetime import datetime, timezone
import os


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo):
        activity_rate = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)
        activity_rate_serialized = ActivityRateIssueSerializers(
            activity_rate, many=True)

        if(not activity_rate):
            open_issues, closed_issues = get_all_issues(owner, repo)

            if(open_issues + closed_issues == ZERO):
                ActivityRateIssue.objects.create(
                    owner=owner,
                    repo=repo,
                    activity_rate=ZERO,
                    date_time=datetime.now(timezone.utc),
                    activity_rate_15_days=ZERO,
                    activity_rate_15_days_metric=ZERO,
                )
            else:
                issues_alive, not_alive = get_issues_15_day(owner, repo)

                if(not_alive != ZERO):
                    activity_rate_15_days = issues_alive / not_alive
                else:
                    activity_rate_15_days = ZERO

                ActivityRateIssue.objects.create(
                    owner=owner,
                    repo=repo,
                    activity_rate=(
                        open_issues / (closed_issues + open_issues)
                    ),
                    date_time=datetime.now(timezone.utc),
                    activity_rate_15_days=activity_rate_15_days,
                    activity_rate_15_days_metric=calculate_metric(
                        issues_alive,
                        not_alive
                    ),
                )

        elif check_datetime(activity_rate[0]):
            open_issues, closed_issues = get_all_issues(owner, repo)
            issues_alive, not_alive = get_issues_15_day(owner, repo)

            if(not_alive != ZERO):
                activity_rate_15_days = issues_alive / not_alive
            else:
                activity_rate_15_days = ZERO

            ActivityRateIssue.objects.filter(owner=owner, repo=repo).update(
                activity_rate=(open_issues / (closed_issues + open_issues)),
                date_time=datetime.now(timezone.utc),
                activity_rate_15_days=activity_rate_15_days,
                activity_rate_15_days_metric=calculate_metric(issues_alive,
                                                              not_alive),
            )

        activity_rate = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)

        activity_rate_serialized = ActivityRateIssueSerializers(
            activity_rate, many=True)

        return Response(activity_rate_serialized.data)


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
