from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import * 


class WelcomingQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request =  requests.get(url + owner + '/' + repo)

        if(github_request.status_code == 200):
            url = URL_COMMIT + 'contributors/different_authors/' + owner + '/' + repo
            contributors_metric = requests.get(url)
            print(contributors_metric.json())

            url = URL_COMMUNITY + 'contribution_guide/' + owner + '/' + repo
            contribution_guide_metric = requests.get(url)
            print(contribution_guide_metric.json())

            url = URL_ISSUES + 'help_wanted/' + owner + '/' + repo
            help_wanted_metrics = requests.get(url)
            print(help_wanted_metrics.json())

            url = URL_ISSUES + 'good_first_issue/' + owner + '/' + repo
            good_first_issue_metrics = requests.get(url)
            print(good_first_issue_metrics.json())

            url = URL_COMMUNITY + 'pull_request_template/' + owner + '/' + repo
            pull_request_template_metrics = requests.get(url)
            print(pull_request_template_metrics.json())

            url = URL_COMMUNITY + 'description/' + owner + '/' + repo
            description_metrics = requests.get(url)
            print(description_metrics.json())

            url = URL_COMMUNITY + 'code_of_conduct/' + owner + '/' + repo
            code_of_conduct_metrics = requests.get(url)
            print(code_of_conduct_metrics.json())

            url = URL_COMMUNITY + 'readme/' + owner + '/' + repo
            readme_metrics = requests.get(url)
            print(readme_metrics.json())

            url = URL_COMMUNITY + 'issue_template/' + owner + '/' + repo
            issue_template_metrics = requests.get(url)
            print(issue_template_metrics.json())

            url = URL_COMMUNITY + 'license/' + owner + '/' + repo
            license_metrics = requests.get(url)
            print(license_metrics.json())
        return Response('ok')