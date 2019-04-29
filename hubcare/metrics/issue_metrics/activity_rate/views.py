import requests
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ActivityRateIssue
from .serializers import ActivityRateIssueSerializers
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

            if(open_issues + closed_issues == 0):
                ActivityRateIssue.objects.create(
                    owner=owner,
                    repo=repo,
                    activity_rate=0,
                    date=datetime.now(timezone.utc),
                    activity_rate_15_days=0,
                    activity_rate_15_days_metric=0,
                )
            else:
                issues_alive, not_alive = get_issues_15_day(owner, repo)
                ActivityRateIssue.objects.create(
                    owner=owner,
                    repo=repo,
                    activity_rate=(
                        open_issues / (closed_issues + open_issues)
                    ),
                    date=datetime.now(timezone.utc),
                    activity_rate_15_days=issues_alive / not_alive,
                    activity_rate_15_days_metric=calculate_metric(
                        issues_alive,
                        not_alive
                    ),
                )

        elif check_datetime(activity_rate[0]):
            open_issues, closed_issues = get_all_issues(owner, repo)
            issues_alive, not_alive = get_issues_15_day(owner, repo)

            ActivityRateIssue.objects.filter(owner=owner, repo=repo).update(
                activity_rate=(open_issues / (closed_issues + open_issues)),
                date=datetime.now(timezone.utc),
                activity_rate_15_days=issues_alive / not_alive,
                activity_rate_15_days_metric=calculate_metric(issues_alive,
                                                              not_alive),
            )

        activity_rate = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)

        activity_rate_serialized = ActivityRateIssueSerializers(
            activity_rate, many=True)

        return Response(activity_rate_serialized.data)


def check_datetime(activity_rate):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - activity_rate.date).days >= 1):
        return True
    return False


def check_datetime_15_days(activity_rate):
    '''
    verifies if the time difference between the issue created and now is
    greater than 15 days
    '''
    activity_rate = datetime.strptime(activity_rate, '%Y-%m-%dT%H:%M:%SZ')
    datetime_now = datetime.now()
    if((datetime_now - activity_rate).days <= 15):
        return True
    return False


def get_issues_15_day(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    page_number = 1
    issues_alive = 0
    issues_not_alive = 0
    u = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues?&page='
    aux = True
    username = os.environ['USERNAME']
    token = os.environ['TOKEN']

    while aux:
        github_request = requests.get(u + str(page_number) + '&per_page=100',
                                      auth=(os.environ['USERNAME'],
                                            os.environ['TOKEN']))
        github_data = github_request.json()

        for activity in github_data:
            print(activity)
            if(check_datetime_15_days(activity['updated_at'])):
                if(activity['state'] == 'open'):
                    issues_alive = issues_alive + 1
                else:
                    # Do nothing
                    pass
            if(activity['state'] == 'open'):
                issues_not_alive = issues_not_alive + 1
            else:
                # Do nothing
                pass

        if(github_data == []):
            aux = False
        print(issues_alive)
        print(issues_not_alive)
        page_number = page_number + 1
    return issues_alive, issues_not_alive


def get_all_issues(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    github_page = requests.get(
        'https://github.com/' + owner + '/' + repo + '/issues')
    find = re.search(r'(.*) Open\n', github_page.text)
    if (find is None):
        return 0, 0
    open_issues = int(find.group(1).replace(',', ''))

    find = re.search(r'(.*) Closed\n', github_page.text)
    closed_issues = int(find.group(1).replace(',', ''))

    return open_issues, closed_issues


def calculate_metric(issues_alive, open_issues):
    '''
    Calculate metrics
    '''
    metric = ((issues_alive / open_issues) - 0.5) * 4

    if metric > 1:
        metric = 1
    elif metric < 0:
        metric = 0

    return metric
