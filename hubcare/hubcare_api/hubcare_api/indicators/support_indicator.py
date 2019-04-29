from hubcare_api.constants import *
import requests
import os


def get_support_indicator(owner, repo):
    url = URL_COMMUNITY + 'readme/' + owner + '/' + repo
    readme_metric = requests.get(url)
    readme_bool = readme_metric.json()[0]['readme']
    readme_int = int(readme_bool)

    url = URL_COMMUNITY + 'issue_template/' + owner + '/' + repo
    issue_temp_metric = requests.get(url)
    issue_temp_bool = issue_temp_metric.json()['issue_templates']
    issue_temp_int = int(issue_temp_bool)

    url = URL_COMMUNITY + 'license/' + owner + '/' + repo
    license_metric = requests.get(url)
    license_bool = license_metric.json()['have_license']
    license_int = int(license_bool)

    url = URL_COMMUNITY + 'description/' + owner + '/' + repo
    description_metric = requests.get(url)
    description_bool = description_metric.json()['description']
    description_int = int(description_bool)

    url = URL_COMMUNITY + 'code_of_conduct/' + owner + '/' + repo
    code_cond_metric = requests.get(url)
    code_cond_bool = code_cond_metric.json()['code_of_conduct']
    code_cond_int = int(code_cond_bool)

    url = URL_COMMUNITY + 'release_note/' + owner + '/' + repo
    release_note_metric = requests.get(url)
    release_note_bool = release_note_metric.json()['response']
    release_note_int = int(release_note_bool)

    url = URL_ISSUE + 'activity_rate/' + owner + '/' + repo
    issue_act_metric = requests.get(url)
    issue_act = issue_act_metric.json()[0]['activity_rate_15_days']
    issue_act_float = float(issue_act)

    support_metric = calculate_support_metric(
        readme_int,
        issue_temp_int,
        license_int,
        description_int,
        code_cond_int,
        release_note_int,
        issue_act_float
    )
    # else:
    #     return False

    return support_metric


def calculate_support_metric(
    readme_int,
    issue_temp_int,
    license_int,
    description_int,
    code_cond_int,
    release_note_int,
    issue_act_float
):
    media = ((issue_act_float - ISSUE_METRIC_ONE) * ISSUE_METRIC_TWO)
    issue_act_float = media
    if(issue_act_float > 1):
        issue_act_float = 1
    elif(issue_act_float < 1):
        issue_act_float = 0

    support_metric = (
        readme_int * HEIGHT_README_SUPPORT
        + issue_temp_int * HEIGHT_ISSUE_TEMPLATE_SUPPORT
        + license_int * HEIGHT_LICENSE_SUPPORT
        + description_int * HEIGHT_DESCRIPTION_SUPPORT
        + code_cond_int * HEIGHT_CODE_OF_CONDUCT_SUPPORT
        + release_note_int * HEIGHT_RELEASE_NOTE_SUPPORT
        + issue_act_float * HEIGHT_ISSUE_ACTIVE_SUPPORT) / SUPPORT_METRIC

    return support_metric
