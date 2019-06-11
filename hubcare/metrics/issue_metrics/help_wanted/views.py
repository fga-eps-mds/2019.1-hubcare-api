from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from help_wanted.models import HelpWanted
from help_wanted.serializers import HelpWantedSerializer
from issue_metrics import constants
from issue_metrics.functions import count_all_label
import requests
import json
import os

from datetime import datetime, timezone


class HelpWantedView(APIView):
    def get(self, request, owner, repo):
        '''
        returns help wanted issue rate
        '''
        help_wanted = HelpWanted.objects.get(
            owner=owner,
            repo=repo
        )
        serializer = HelpWantedSerializer(help_wanted)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, owner, repo):
        '''
        Create help wanted object
        '''
        data = HelpWanted.objects.filter(
            owner=owner,
            repo=repo
        )
        if data:
            serializer = HelpWantedSerializer(data[0])
            return Response(serializer.data, status=status.HTTP_200_OK)

        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, help_wanted_issues = self.get_total_helpwanted(url)
        if total_issues == 0:
            rate = 0
        else:
            rate = help_wanted_issues/total_issues
        data = HelpWanted.objects.create(
            owner=owner,
            repo=repo,
            total_issues=total_issues,
            help_wanted_issues=help_wanted_issues,
            help_wanted_rate=rate,
            help_wanted_max_rate=constants.HELP_WANTED_MAX_RATE
        )

        serializer = HelpWantedSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, owner, repo):
        '''
        Update help hanted object
        '''
        url = '{0}{1}/{2}'.format(
            constants.MAIN_URL,
            owner,
            repo
        )
        total_issues, help_wanted_issues = self.get_total_helpwanted(url)
        if total_issues == 0:
            rate = 0
        else:
            rate = help_wanted_issues/total_issues
        data = HelpWanted.objects.get(
            owner=owner,
            repo=repo
        )
        data.total_issues = total_issues
        data.help_wanted_issues = help_wanted_issues
        data.help_wanted_rate = rate
        data.help_wanted_max_rate = constants.HELP_WANTED_MAX_RATE
        data.save()

        serializer = HelpWantedSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
