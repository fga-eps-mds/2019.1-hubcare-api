from hubcare_api.constants import *
import requests
import os


def get_active_indicator(owner, repo, metric):
    community_metric = metric['community_metric']
    pull_request_metric = metric['pull_request_metric']
    issue_metric = metric['issue_metric']
    commit_metric = metric['commit_metric']

    contributors_int = int(commit_metric['differents_authors'])
    release_note_int = int(community_metric['release_note'])
    pr_qua_float = float(pull_request_metric['acceptance_quality'])
    commit_week_int = commit_metric['total_commits']
    activity_rate = float(issue_metric['activity_rate'])
    active_metric = calculate_active_metric(
        release_note_int,
        contributors_int,
        commit_week_int,
        pr_qua_float,
        activity_rate
    )

    return active_metric


def calculate_active_metric(
    release_note_int,
    contributors_int,
    commit_week_int,
    pr_qua_float,
    activity_rate
):
    contributors_int = contributors_int * METRIC_CONTRIBUTOR
    if(contributors_int > 1):
        contributors_int = 1

    commit_week_int = commit_week_int * METRIC_COMMIT
    if(commit_week_int > 1):
        commit_week_int = 1

    activity_rate = ((activity_rate - ISSUE_METRIC_ONE) * ISSUE_METRIC_TWO)
    if activity_rate > 1:
        activity_rate = 1
    elif activity_rate < 1:
        activity_rate = 0

    ACT_MET_QUEST = ACTIVE_METRIC_QUESTION
    active_metric = (
                    release_note_int * WEIGHT_RELEASE_NOTE_ACTIVE
                    + contributors_int * WEIGHT_CONTRIBUTOR_ACTIVE
                    + commit_week_int * WEIGHT_COMMIT_WEEK_ACTIVE
                    + pr_qua_float * WEIGHT_PR_QUALITY_1
                    + activity_rate * WEIGHT_ACT_MET_1) / ACT_MET_QUEST

    return active_metric
