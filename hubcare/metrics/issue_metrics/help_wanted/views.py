from rest_framework.views import APIView
from rest_framework.response import Response
from help_wanted.models import HelpWanted
from help_wanted.serializers import HelpWantedSerializer
from datetime import datetime, timezone
from issue_metrics import constants
from issue_metrics.functions \
    import check_datetime, get_metric_help_wanted, count_all_label
import requests
import json
import os


class HelpWantedView(APIView):
    def get(self, request, owner, repo):
        '''
        returns help wanted issue rate
        '''
        help_wanted = HelpWanted.objects.all().filter(owner=owner, repo=repo)
        url = constants.MAIN_URL + owner + '/' + repo
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

        return Response(get_metric_help_wanted(HelpWanted, owner, repo))

    def get_total_helpwanted(self, url):
        '''
        returns the number of all issues and the issues with
        help wanted label
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        total_issues = 0
        help_wanted_issues = 0
        info_repo = requests.get(url, auth=(username, token)).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.LABEL_HELP_ESPACE_WANTED
        result = requests.get(label_url + page,
                              auth=(username, token)).json()

        '''
        checks possibilities for different aliases of help wanted
        '''
        if result:
            help_wanted_issues = count_all_label(label_url, result)
        else:
            label_url = url + constants.LABEL_HELPWANTED
            result = requests.get(label_url + page,
                                  auth=(username, token)).json()
            if result:
                help_wanted_issues = count_all_label(
                    label_url,
                    result
                )
            else:
                label_url = url + constants.LABEL_HELP_WANTED
                result = requests.get(label_url + page,
                                      auth=(username, token)).json()
                if result:
                    help_wanted_issues = count_all_label(
                        label_url,
                        result
                    )
        return total_issues, help_wanted_issues
