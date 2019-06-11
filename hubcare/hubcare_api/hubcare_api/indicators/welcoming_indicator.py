from hubcare_api.constants import *
import requests
import os


def get_welcoming_indicator(owner, repo, metric):
    community_metric = metric['community_metric']
    pull_request_metric = metric['pull_request_metric']
    issue_metric = metric['issue_metric']
    commit_metric = metric['commit_metric']

    cont_guide_int = int(community_metric['contribution_guide'])
    help_float = float(issue_metric['help_wanted_rate'])
    good_float = float(issue_metric['good_first_issue_rate'])
    prt_int = int(community_metric['pull_request_template'])
    description_int = int(community_metric['description'])
    code_cond_int = int(community_metric['code_of_conduct'])
    readme_int = int(community_metric['readme'])
    issue_temp_int = int(community_metric['issue_template'])
    license_int = int(community_metric['license'])
    act_rate_float = float(issue_metric['activity_rate'])
    pr_qua_float = float(pull_request_metric['acceptance_quality'])
    contributors_int = int(commit_metric['differents_authors'])

    welcoming_metric = calculate_welcoming_metric(
        contributors_int,
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
    contributors_int,
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
    contributors_int = contributors_int * METRIC_CONTRIBUTOR
    if(contributors_int > 1):
        contributors_int = 1

    media = ((act_rate_float - ISSUE_METRIC_ONE) * ISSUE_METRIC_TWO)
    act_rate_float = media
    if(act_rate_float > 1):
        act_rate_float = 1
    if(act_rate_float < 1):
        act_rate_float = 0

    WEIGHT_SUPPORT_2 = WEIGHT_ISSUE_ACTIVE_SUPPORT_QUESTION_2
    welcoming_metric = (
        contributors_int * WEIGHT_CONTRIBUTORS_WELCO
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
