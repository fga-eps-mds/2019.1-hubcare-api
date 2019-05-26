from hubcare_api.constants import *
import requests
import os


def get_welcoming_indicator(owner, repo, metric):

    cont_guide_int = int(metric['contribution_guide'])
    help_float = float(metric['help_wanted_issues'])
    good_float = float(metric['good_first_issue'])
    prt_int = int(metric['pull_request_template'])
    description_int = int(metric['description'])
    code_cond_int = int(metric['code_of_conduct'])
    readme_int = int(metric['readme'])
    issue_temp_int = int(metric['issue_template'])
    license_int = int(metric['license']   ) 
    act_rate_float = float(metric['activity_rate_15_days'])
    pr_qua_float = float(metric['acceptance_quality'])
    # url_authors = 'contributors/'
    # url = URL_COMMIT + url_authors + owner + '/' + repo
    # cont_metric = requests.get(url)
    # cont_total = len(cont_metric.json())
    # cont_int = int(cont_total)

    welcoming_metric = calculate_welcoming_metric(
        # cont_int,
        cont_guide_int,
        help_float,
        good_float,
        prt_int,
        description_int,
        code_cond_int,
        readme_int,
        issue_temp_int,
        license_int,
        act_rate_float,
        pr_qua_float
    )

    return welcoming_metric


def calculate_welcoming_metric(
    # cont_int,
    cont_guide_int,
    help_float,
    good_float,
    prt_int,
    description_int,
    code_cond_int,
    readme_int,
    issue_temp_int,
    license_int,
    act_rate_float,
    pr_qua_float
):
    # cont_int = cont_int * METRIC_CONTRIBUTOR
    # if(cont_int > 1):
    #     cont_int = 1

    media = ((act_rate_float - ISSUE_METRIC_ONE) * ISSUE_METRIC_TWO)
    act_rate_float = media
    if(act_rate_float > 1):
        act_rate_float = 1
    if(act_rate_float < 1):
        act_rate_float = 0

    WEIGHT_SUPPORT_2 = WEIGHT_ISSUE_ACTIVE_SUPPORT_QUESTION_2
    welcoming_metric = (
        # cont_int * WEIGHT_CONTRIBUTORS_WELCO
        + cont_guide_int * WEIGHT_CONTRIBUTION_GUIDE_WELCO
        + help_float * WEIGHT_HELP_WANTED_WELCO
        + good_float * WEIGHT_GOOD_FIRST_ISSUE_WELCO
        + prt_int * WEIGHT_PR_TEMPLATE_WELCO
        + description_int * WEIGHT_DESCRIPTION_WELCO
        + code_cond_int * WEIGHT_CODE_OF_CONDUCT_WELCO
        + readme_int * WEIGHT_README_WELCO
        + issue_temp_int * WEIGHT_ISSUE_TEMPLATE_WELCO
        + license_int * WEIGHT_LICENSE_WELCO
        + act_rate_float * WEIGHT_ACT_MET_2
        + pr_qua_float * WEIGHT_PR_QUALITY) / WELCOMING_METRIC_QUESTION

    return welcoming_metric
