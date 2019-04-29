from hubcare_api.constants import *
import requests
import os


def get_active_indicator(owner, repo):
    url = URL_COMMUNITY + 'release_note/' + owner + '/' + repo
    release_note_metric = requests.get(url)
    release_note_bool = release_note_metric.json()['response']
    release_note_int = int(release_note_bool)

    url_authors = 'contributors/different_authors/'
    url = URL_COMMIT + url_authors + owner + '/' + repo
    contributors_metric = requests.get(url)
    contributors_total = len(contributors_metric.json())
    contributors_int = int(contributors_total)

    url = URL_COMMIT + 'commit_week/commit_week/' + owner + '/' + repo
    commit_week_metric = requests.get(url)
    commit_week_sum = commit_week_metric.json()['sum']
    commit_week_int = int(commit_week_sum)

    url_authors = 'acceptance_quality/'
    url = URL_PR + url_authors + owner + '/' + repo
    pr_qua_metric = requests.get(url)
    pr_qua_str = pr_qua_metric.json()[0]['metric']
    pr_qua_float = float(pr_qua_str)

    url_authors = 'activity_rate/'
    url = URL_ISSUES + url_authors + owner + '/' + repo
    act_rate_metric = requests.get(url)
    act_rate_str = act_rate_metric.json()[0]['activity_rate_15_days']
    act_rate_float = float(act_rate_str)

    active_metric = calculate_active_metric(
        release_note_int,
        contributors_int,
        commit_week_int,
        pr_qua_float,
        act_rate_float
    )

    return active_metric


def calculate_active_metric(
    release_note_int,
    contributors_int,
    commit_week_int,
    pr_qua_float,
    act_rate_float
):
    contributors_int = contributors_int * METRIC_CONTRIBUTOR
    if(contributors_int > 1):
        contributors_int = 1

    commit_week_int = commit_week_int * METRIC_COMMIT
    if(commit_week_int > 1):
        commit_week_int = 1

    media = ((act_rate_float - ISSUE_METRIC_ONE) * ISSUE_METRIC_TWO)
    act_rate_float = media
    if(act_rate_float > 1):
        act_rate_float = 1
    if(act_rate_float < 1):
        act_rate_float = 0

    ACT_MET_QUEST = ACTIVE_METRIC_QUESTION
    active_metric = (
                    release_note_int * HEIGHT_RELESE_NOTE_ACTIVE
                    + contributors_int * HEIGHT_CONTRIBUTOR_ACTIVE
                    + commit_week_int * HEIGHT_COMMIT_WEEK_ACTIVE
                    + pr_qua_float * HEIGHT_PR_QUALITY_1
                    + act_rate_float * HEIGHT_ACT_MET_1) / ACT_MET_QUEST

    return active_metric
