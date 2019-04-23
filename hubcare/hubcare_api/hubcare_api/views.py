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
            readme_int = int(readme_metric.json()[0]['readme'])
    
            url = URL_COMMMUNITY + 'issue_template/' + owner + '/' + repo
            issue_template_metric = requests.get(url)
            issue_template_int = int(issue_template_metric.json()['issue_templates'])

            url = URL_COMMMUNITY + 'license/' + owner + '/' + repo
            license_metric = requests.get(url)
            license_int = int(license_metric.json()['have_license'])

            url = URL_COMMMUNITY + 'description/' + owner + '/' + repo
            description_metric = requests.get(url)
            description_int = int(description_metric.json()['description'])

            url = URL_COMMMUNITY + 'code_of_conduct/' + owner + '/' + repo
            code_of_conduct_metric = requests.get(url)
            code_of_conduct_int = int(code_of_conduct_metric.json()['code_of_conduct'])

            url = URL_COMMMUNITY + 'release_note/' + owner + '/' + repo
            release_note_metric = requests.get(url)
            release_note_int = int(release_note_metric.json()['response'])

            support_metric = calculate_support_metric(readme_int,
                                                    issue_template_int,
                                                    license_int,
                                                    description_int,
                                                    code_of_conduct_int,
                                                    release_note_int
            )

        else:
            raise Http404

        return Response(support_metric)

def calculate_support_metric(readme_int,
                            issue_template_int,
                            license_int,
                            description_int,
                            code_of_conduct_int,
                            release_note_int
                        ):

    support_metric = (readme_int*HEIGHT_README_SUPPORT
                    +issue_template_int*HEIGHT_ISSUE_TEMPLATE_SUPPORT
                    +license_int*HEIGHT_LICENSE_SUPPORT
                    +description_int*HEIGHT_DESCRIPTION_SUPPORT
                    +code_of_conduct_int*HEIGHT_CODE_OF_CONDUCT_SUPPORT
                    +release_note_int*HEIGHT_RELEASE_NOTE_SUPPORT)/16

    return support_metric
