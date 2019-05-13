from rest_framework.views import APIView
from rest_framework.response import Response
from good_first_issue.models import GoodFirstIssue
from good_first_issue.serializers import GoodFirstIssueSerializer
from datetime import datetime, timezone
from issue_metrics import constants
from issue_metrics.functions \
    import check_datetime, get_metric_good_first_issue, count_all_label
import requests
import json
import os


class GoodFirstIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        returns good first issue rate
        '''

        good_first_issues = GoodFirstIssue.objects.all().filter(
            owner=owner,
            repo=repo
        )
        url = constants.MAIN_URL + owner + '/' + repo
        if(not good_first_issues):
            total_issues, good_first_issue = self.get_total_goodfirstissue(url)
            GoodFirstIssue.objects.create(
                owner=owner,
                repo=repo,
                total_issues=total_issues,
                good_first_issue=good_first_issue,
                date_time=datetime.now(
                    timezone.utc
                )
            )
        elif check_datetime(good_first_issues[0]):
            good_first_issues = GoodFirstIssue.objects.get(
                owner=owner,
                repo=repo
            )
            total_issues, good_first_issue = self.get_total_goodfirstissue(url)
            GoodFirstIssue.objects.filter(owner=owner, repo=repo).update(
                total_issues=total_issues,
                good_first_issue=good_first_issue,
                date_time=datetime.now(
                    timezone.utc
                )
            )
        return Response(
            get_metric_good_first_issue(
                GoodFirstIssue,
                owner,
                repo
            )
        )

    def get_total_goodfirstissue(self, url):
        '''
        returns the number of all issues and the issues with
        good first issue label
        '''
        username = os.environ['NAME']
        token = os.environ['TOKEN']

        total_issues = constants.ZERO
        good_first_issue = constants.ZERO
        info_repo = requests.get(url, auth=(username,
                                            token)).json()
        total_issues = info_repo["open_issues_count"]
        page = '&page=1'
        label_url = url + constants.LABEL_GOOD_FIRST_ISSUE_SPACES
        result = requests.get(label_url + page,
                              auth=(username,
                                    token)).json()

        '''
        checks possibilities for different aliases of good first issue
        '''
        if result:
            good_first_issue = count_all_label(
                label_url,
                result
            )
        else:
            label_url = url + constants.LABEL_GOODFIRSTISSUE
            result = requests.get(label_url + page,
                                  auth=(username,
                                        token)).json()
            if result:
                good_first_issue = count_all_label(
                    label_url,
                    result
                )
            else:
                label_url = url + constants.LABEL_GOOD_FIRST_ISSUE
                result = requests.get(label_url + page,
                                      auth=(username,
                                            token)).json()
                if result:
                    good_first_issue = count_all_label(
                        label_url,
                        result
                    )
        return total_issues, good_first_issue
