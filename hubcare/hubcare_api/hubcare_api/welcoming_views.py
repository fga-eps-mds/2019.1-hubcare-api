from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import *


class WelcomingQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        username = 'Brian2397'
        token = 'ed76a29b4bde2a0ec415b41fd51e2d740be50941'
        github_request = requests.get(url + owner + '/' + repo, auth=(username, token))

        if(github_request.status_code is 200):
            url_authors = 'contributors/different_authors/'
            url = URL_COMMIT + url_authors + owner + '/' + repo
            cont_metric = requests.get(url)
            cont_total = len(cont_metric.json())
            cont_int = int(cont_total)

            url_authors = 'contribution_guide/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            cont_guide_metric = requests.get(url)
            cont_guide_bool = cont_guide_metric.json()[0]['contribution_guide']
            cont_guide_int = int(cont_guide_bool)

            url_authors = 'help_wanted/'
            url = URL_ISSUES + url_authors + owner + '/' + repo
            help_metric = requests.get(url)
            help_rate = help_metric.json()['rate']
            help_float = float(help_rate)

            url_authors = 'good_first_issue/'
            url = URL_ISSUES + url_authors + owner + '/' + repo
            good_metric = requests.get(url)
            good_rate = good_metric.json()['rate']
            good_float = float(good_rate)

            url_authors = 'pull_request_template/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            prt_metric = requests.get(url)
            prt_bool = prt_metric.json()['pull_request_template']
            prt_int = int(prt_bool)

            url_authors = 'description/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            description_metric = requests.get(url)
            description_bool = description_metric.json()['description']
            description_int = int(description_bool)

            url_authors = 'code_of_conduct/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            code_cond_metric = requests.get(url)
            code_cond_bool = code_cond_metric.json()['code_of_conduct']
            code_cond_int = int(code_cond_bool)

            url_authors = 'readme/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            readme_metrics = requests.get(url)
            readme_bool = readme_metrics.json()[0]['readme']
            readme_int = int(readme_bool)

            url_authors = 'issue_template/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            issue_temp_metric = requests.get(url)
            issue_temp_bool = issue_temp_metric.json()['issue_templates']
            issue_temp_int = int(issue_temp_bool)

            url_authors = 'license/'
            url = URL_COMMUNITY + url_authors + owner + '/' + repo
            license_metric = requests.get(url)
            license_bool = license_metric.json()['have_license']
            license_int = int(license_bool)

            welcoming_metric = calculate_welcoming_metric(
                cont_int,
                cont_guide_int,
                help_float,
                good_float,
                prt_int,
                description_int,
                code_cond_int,
                readme_int,
                issue_temp_int,
                license_int
            )

        return Response(welcoming_metric)


def calculate_welcoming_metric(
    cont_int,
    cont_guide_int,
    help_float,
    good_float,
    prt_int,
    description_int,
    code_cond_int,
    readme_int,
    issue_temp_int,
    license_int
):
    cont_int = cont_int*METRIC_CONTRIBUTOR
    if(cont_int > 1):
        cont_int = 1
    welcoming_metric = (
        cont_int*HEIGHT_CONTRIBUTORS_WELCO
        + cont_guide_int*HEIGHT_CONTRIBUTION_GUIDE_WELCO
        + help_float*HEIGHT_HELP_WANTED_WELCO
        + good_float*HEIGHT_GOOD_FIRST_ISSUE_WELCO
        + prt_int*HEIGHT_PR_TEMPLATE_WELCO
        + description_int*HEIGHT_DESCRIPTION_WELCO
        + code_cond_int*HEIGHT_CODE_OF_CONDUCT_WELCO
        + readme_int*HEIGHT_README_WELCO
        + issue_temp_int*HEIGHT_ISSUE_TEMPLATE_WELCO
        + license_int*HEIGHT_LICENSE_WELCO)/23

    return welcoming_metric
