from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from help_wanted.models import HelpWanted
from help_wanted.serializers import HelpWantedSerializer
from issue_metrics import constants
from issue_metrics.functions \
    import get_metric_help_wanted, count_all_label
import requests
import json
import os

from datetime import datetime, timezone


class HelpWantedView(APIView):
    def get(self, request, owner, repo):
        '''
        returns help wanted issue rate
        '''

        try:
            help_wanted = HelpWanted.objects.all().filter(
                owner=owner,
                repo=repo
            )[0]
            serializer = HelpWantedSerializer(help_wanted)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('There is no repository for this metric',
                            status=status.HTTP_400_BAD_REQUEST)

        # return Response(get_metric_help_wanted(HelpWanted, owner, repo))

    def post(self, request, owner, repo):
        
        print('time help wanted 1', datetime.now())
        url = constants.MAIN_URL + owner + '/' + repo
        total_issues, help_wanted_issues = self.get_total_helpwanted(url)
        data = {
            'owner': owner,
            'repo': repo,
            'total_issues': total_issues,
            'help_wanted_issues': help_wanted_issues
        }

        serializer = HelpWantedSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print('time help wanted 2', datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Error on creating help wanted metric',
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, owner, repo):
        help_wanted_object = HelpWanted.objects.filter(
            owner=owner,
            repo=repo
        )[0]
        url = constants.MAIN_URL + owner + '/' + repo
        total_issues, help_wanted_issues = self.get_total_helpwanted(url)
        data = {
            'total_issues': total_issues,
            'help_wanted_issues': help_wanted_issues
        }

        serializer = HelpWantedSerializer(help_wanted_object, data,
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Error on updating help wanted metric',
                            status=status.HTTP_400_BAD_REQUEST)

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
