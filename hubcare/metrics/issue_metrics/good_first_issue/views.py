from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from good_first_issue.models import GoodFirstIssue
from good_first_issue.serializers import GoodFirstIssueSerializer
from issue_metrics import constants
from issue_metrics.functions \
    import get_metric_good_first_issue, count_all_label
import requests
import json
import os

from datetime import datetime, timezone


class GoodFirstIssueView(APIView):
    def get(self, request, owner, repo):
        '''
        Returns good first issue data
        '''

        good_first_issue = GoodFirstIssue.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = GoodFirstIssueSerializer(good_first_issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):
        '''
        Creates good first issue data for repository
        '''

        print('time good_first_issue 1', datetime.now())
        data = GoodFirstIssue.objects.filter(
            owner=owner,
            repo=repo
        )
        if data:
            serializer = GoodFirstIssueSerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, good_first_issue = self.get_total_goodfirstissue(url)
        data = GoodFirstIssue.objects.create(
            owner=owner,
            repo=repo,
            total_issues=total_issues,
            good_first_issue=good_first_issue
        )

        serializer = GoodFirstIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo):
        '''
        Updates good first issue data for repository
        '''

        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, good_first_issue = self.get_total_goodfirstissue(url)
        data = GoodFirstIssue.objects.get(
            owner=owner,
            repo=repo
        )
        data.total_issues = total_issues
        data.good_first_issue = good_first_issue
        data.save()

        serializer = GoodFirstIssueSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
