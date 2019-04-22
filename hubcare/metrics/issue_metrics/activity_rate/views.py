import requests
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ActivityRateIssue
from .serializers import ActivityRateIssueSerializers
from datetime import datetime, timezone


class ActivityRateIssueView(APIView):
    def get(self, request, owner, repo):
        activity_rate = ActivityRateIssue.objects.all().filter(
            owner=owner, repo=repo)
        activity_rate_serialized = ActivityRateIssueSerializers(
            activity_rate, many=True)

        if(not activity_rate):
            open_issues, closed_issues = get_all_issues(owner, repo)
            issues_comment, issues_no_comment = get_issues_15_day(owner, repo)

            ActivityRateIssue.objects.create(
                owner=owner,
                repo=repo,
                activity_rate=(open_issues / (closed_issues + open_issues)),
                date=datetime.now(timezone.utc),
                activity_rate_15_days=issues_comment / (issues_comment +
                                                        issues_no_comment),
            )
        elif check_datetime(activity_rate[0]):
            issues_comment, issues_no_comment = get_issues_15_day(owner, repo)

            ActivityRateIssue.objects.filter(owner=owner, repo=repo).update(
                activity_rate=(open_issues / (closed_issues + open_issues)),
                date=datetime.now(timezone.utc),
                activity_rate_15_days=len(issues_comment) / (issues_comment +
                                                             issues_no_comment),
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
    issues_comment = []
    issues_no_comment = []
    u = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues?&page='
    aux = True

    while aux:
        github_request = requests.get(u + str(page_number) + '&per_page=100')
        github_data = github_request.json()

        for activity in github_data:
            print(activity)
            if(check_datetime_15_days(activity['created_at'])):
                if(activity['state'] == 'open' and activity['comments'] == 0):
                    issues_no_comment.append(activity)
                else:
                    issues_comment.append(activity)
            else:
                aux = False
                break
        if(github_data == []):
            aux = False

        page_number = page_number + 1
    return len(issues_comment), len(issues_no_comment)


def get_all_issues(owner, repo):
    '''
    Get all the issues in the last 15 days
    '''
    github_page = requests.get(
        'https://github.com/' + owner + '/' + repo + '/issues')
    find = re.search(r'(.*) Open\n', github_page.text)
    open_issues = int(find.group(1).replace(',', ''))

    find = re.search(r'(.*) Closed\n', github_page.text)
    closed_issues = int(find.group(1).replace(',', ''))

    return open_issues, closed_issues
