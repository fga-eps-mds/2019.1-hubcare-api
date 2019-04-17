from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from issues.models.help_wanted_models import HelpWanted
from issues.serializers.help_wanted_serializers import HelpWantedSerializer
from datetime import datetime, timezone
import requests
import json
from issues import constants


class HelpWantedView(APIView):
    def get(self, request, owner, repo):
        '''
        returns help wanted issue rate
        '''
        help_wanted = HelpWanted.objects.all().filter(owner=owner, repo=repo)
        if(not help_wanted):
            url = constants.main_url + owner + '/' + repo + '/issues'
            result = requests.get(url)
            issues = result.json()

            if(result.status_code == 404):
                raise Http404
            total_issues, help_wanted_issues = self.count_issues(issues)
            HelpWanted.objects.create(
                owner=owner,
                repo=repo,
                total_issues=total_issues,
                help_wanted_issues=help_wanted_issues,
                date_time=datetime.now(timezone.utc)
            )
        elif check_datetime(help_wanted[0]):
            help_wanted = HelpWanted.objects.get(owner=owner, repo=repo)
            result = requests.get(url)
            issues = issues.json()

            if(result.status_code == 404):
                raise Http404
            else:
                total_issues, help_wanted_issues = self.count_issues(issues)
                HelpWanted.objects.filter(owner=owner, repo=repo).update(
                    total_issues=total_issues,
                    help_wanted_issues=help_wanted_issues,
                    date_time=datetime.now(timezone.utc)
                )

        return Response(self.get_metric(owner, repo))

    def count_issues(self, issues):
        '''
        counts the number of all issues and all issues with help wanted label
        '''
        total_issues = 0
        help_wanted_issues = 0
        for i in issues:
            total_issues += 1
            labels = i['labels']
            help_wanted_issues += self.check_help_wanted(labels)
        return total_issues, help_wanted_issues

    def check_help_wanted(self, labels):
        '''
        verifies if there is a help wanted label in labels
        '''
        for i in labels:
            name = i['name'].upper().replace(' ', '')
            if name in constants.labels_help_wanted:
                return 1
        return 0

    def get_metric(self, owner, repo):
        '''
        returns the metric of the repository
        '''

        help_wanted = HelpWanted.objects.all().filter(
            owner=owner,
            repo=repo
        )[0]
        rate = help_wanted.help_wanted_issues/help_wanted.total_issues
        rate = '{"rate":\"' + str(rate) + '"}'
        rate_json = json.loads(rate)
        return rate_json


def check_datetime(help_wanted):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if((datetime_now - help_wanted.date_time).days >= 1):
        return True
    return False
