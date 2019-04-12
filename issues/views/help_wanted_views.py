from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from issues.models.help_wanted_models import HelpWanted
from issues.serializers.help_wanted_serializers import HelpWantedSerializer
from datetime import datetime, timezone
import requests
import json

# Create your views here.

class HelpWantedView(APIView):
    def get(self,request,owner,repo):
        """
        returns help wanted issue rate
        """

        url = 'https://api.github.com/repos/' + owner + '/' + repo + '/issues'
        help_wanted = HelpWanted.objects.all().filter(owner=owner, repo=repo)
        if(not help_wanted):
            issues = requests.get(url)
            issues = issues.json()
            total_issues = 0
            help_wanted_issues = 0
            for i in issues:
                total_issues += 1
                labels = i["labels"]
                help_wanted_issues += self.check_help_wanted(labels) 

            HelpWanted.objects.create(
                owner=owner,
                repo=repo,
                total_issues=total_issues,
                help_wanted_issues=help_wanted_issues,
                date_time=datetime.now(timezone.utc)
            )
        return Response(self.get_metric(owner,repo))


    def check_help_wanted(self,labels):
        """
        verifies if there is a help wanted label in labels
        """

        for i in labels:
            name = i["name"].upper()
            if name == "HELPWANTED" or name == "HELP_WANTED" or name == "HELP WANTED":
                return 1
        return 0

    def get_metric(self,owner,repo):
        """
        returns the metric of the repository
        """
        help_wanted = HelpWanted.objects.all().filter(owner=owner,repo=repo)[0]
        rate = help_wanted.help_wanted_issues/help_wanted.total_issues
        rate = "{\"rate\":\"" + str(rate) + "\"}"
        rate_json = json.loads(rate)
        return rate_json
