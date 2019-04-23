from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from hubcare_api.constants import * 


class SupportQuestion(APIView):
    def get(self, request, owner, repo):
        url = 'https://api.github.com/repos/'
        github_request = requests.get(url + owner + '/' + repo)

        if(github_request.status_code == 200):
            url = URL_COMMMUNITY + 'readme/' + owner + '/' + repo
            readme_metric = requests.get(url)
            print(readme_metric.json()[0]['readme'])
            x = int(readme_metric.json()[0]['readme'])
    
            url = URL_COMMMUNITY + 'issue_template/' + owner + '/' + repo
            issue_template_metric = requests.get(url)
            print(issue_template_metric.json()['issue_templates'])
            y = int(issue_template_metric.json()['issue_templates'])

            url = URL_COMMMUNITY + 'license/' + owner + '/' + repo
            license_metric = requests.get(url)
            print(license_metric.json()['have_license'])
            z = int(license_metric.json()['have_license'])

            url = URL_COMMMUNITY + 'description/' + owner + '/' + repo
            description_metric = requests.get(url)
            print(description_metric.json()['description'])
            w = int(description_metric.json()['description'])

            url = URL_COMMMUNITY + 'code_of_conduct/' + owner + '/' + repo
            code_of_conduct_metric = requests.get(url)
            print(code_of_conduct_metric.json()['code_of_conduct'])
            u = int(code_of_conduct_metric.json()['code_of_conduct'])

            url = URL_COMMMUNITY + 'release_note/' + owner + '/' + repo
            release_note_metric = requests.get(url)
            print(release_note_metric.json()['response'])
            v = int(release_note_metric.json()['response'])

            support_metric = calculate_support_metric(x, y, z, w, u, v)

        else:
            raise Http404

        return Response(support_metric)

def calculate_support_metric(readme_metric,
                            issue_template_metric,
                            license_metric,
                            description_metric,
                            code_of_conduct_metric,
                            release_note_metric
                        ):

    support_metric = (readme_metric*HEIGHT_README_SUPPORT
                    +issue_template_metric*HEIGHT_ISSUE_TEMPLATE_SUPPORT
                    +license_metric*HEIGHT_LICENSE_SUPPORT
                    +description_metric*HEIGHT_DESCRIPTION_SUPPORT
                    +code_of_conduct_metric*HEIGHT_CODE_OF_CONDUCT_SUPPORT
                    +release_note_metric*HEIGHT_RELEASE_NOTE_SUPPORT)/16

    return support_metric
