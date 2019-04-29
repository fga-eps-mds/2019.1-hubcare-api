from rest_framework.views import APIView
from rest_framework.response import Response
from help_wanted.models import HelpWanted
from help_wanted.serializers import HelpWantedSerializer
from datetime import datetime, timezone
from issue_metrics import constants
import requests
import json
import os


class HelpWantedView(APIView):
    def get(self, request, owner, repo):
        '''
        returns help wanted issue rate
        '''
        help_wanted = HelpWanted.objects.all().filter(owner=owner, repo=repo)
        url = constants.main_url + owner + '/' + repo
        if(not help_wanted):
            total_issues, help_wanted_issues = self.get_total_helpwanted(url)
            HelpWanted.objects.create(
                owner=owner,
                repo=repo,
                total_issues=total_issues,
                help_wanted_issues=help_wanted_issues,
                date_time=datetime.now(timezone.utc)
            )
        elif check_datetime(help_wanted[0]):
            help_wanted = HelpWanted.objects.get(owner=owner, repo=repo)
            total_issues, help_wanted_issues = self.get_total_helpwanted(url)
            HelpWanted.objects.filter(owner=owner, repo=repo).update(
                total_issues=total_issues,
                help_wanted_issues=help_wanted_issues,
                date_time=datetime.now(timezone.utc)
            )

        return Response(self.get_metric(owner, repo))

    def get_total_helpwanted(self, url):
        '''
        returns the number of all issues and the issues with
        help wanted label
        '''
        total_issues = 0
        help_wanted_issues = 0
        info_repo = requests.get(url, auth=(os.environ['USERNAME'],
                                            os.environ['TOKEN'])).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.label_help_espace_wanted
        result = requests.get(label_url + page,
                              auth=(os.environ['USERNAME'],
                                    os.environ['TOKEN'])).json()

        '''
        checks possibilities for different aliases of help wanted
        '''
        if result:
            help_wanted_issues = self.count_all_helpwanted(label_url, result)
        else:
            label_url = url + constants.label_helpwanted
            result = requests.get(label_url + page,
                                  auth=(os.environ['USERNAME'],
                                        os.environ['TOKEN'])).json()
            if result:
                help_wanted_issues = self.count_all_helpwanted(
                    label_url,
                    result
                )
            else:
                label_url = url + constants.label_help_wanted
                result = requests.get(label_url + page,
                                      auth=(os.environ['USERNAME'],
                                            os.environ['TOKEN'])).json()
                if result:
                    help_wanted_issues = self.count_all_helpwanted(
                        label_url,
                        result
                    )
        return total_issues, help_wanted_issues

    def count_all_helpwanted(self, url, result):
        '''
        returns the number of help wanted issues in all pages
        '''
        count = 1
        page = '&page='
        help_wanted_issues = 0
        while result:
            count += 1
            help_wanted_issues += len(result)
            result = requests.get(url + page + str(count),
                                  auth=(os.environ['USERNAME'],
                                        os.environ['TOKEN'])).json()
        return help_wanted_issues

    def get_metric(self, owner, repo):
        '''
        returns the metric of the repository
        '''
        help_wanted = HelpWanted.objects.all().filter(
            owner=owner,
            repo=repo
        )[0]
        if help_wanted.total_issues != 0:
            rate = help_wanted.help_wanted_issues / help_wanted.total_issues
        else:
            rate = 0.0
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
