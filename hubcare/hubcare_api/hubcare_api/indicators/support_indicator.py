from hubcare_api.constants import *
import requests
import os


def get_support_indicator(owner, repo, metric):
    metric_community = metric['community_metric']
    metric_issue = metric['issue_metric']

    readme_int = int(metric_community['readme'])
    issue_temp_int = int(metric_community['issue_template'])
    license_int = int(metric_community['license'])
    description_int = int(metric_community['description'])
    code_cond_int = int(metric_community['code_of_conduct'])
    release_note_int = int(metric_community['release_note'])
    issue_act_float = float(metric_issue['activity_rate'])

    support_metric = calculate_support_metric(
        readme_int,
        issue_temp_int,
        license_int,
        description_int,
        code_cond_int,
        release_note_int,
        issue_act_float
    )

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
        readme_int * WEIGHT_README_SUPPORT
        + issue_temp_int * WEIGHT_ISSUE_TEMPLATE_SUPPORT
        + license_int * WEIGHT_LICENSE_SUPPORT
        + description_int * WEIGHT_DESCRIPTION_SUPPORT
        + code_cond_int * WEIGHT_CODE_OF_CONDUCT_SUPPORT
        + release_note_int * WEIGHT_RELEASE_NOTE_SUPPORT
        + issue_act_float * WEIGHT_ISSUE_ACTIVE_SUPPORT) / SUPPORT_METRIC

    return support_metric
