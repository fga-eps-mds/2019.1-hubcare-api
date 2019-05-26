from hubcare_api.constants import *
from hubcare_api.services.request import Request


def get_metric(owner, repo, request_type):

    r = Request()
    url_activity = get_url('activity_rate/', owner, repo)
    url_help_wanted = get_url('help_wanted/', owner, repo)
    url_good_first_issue = get_url('good_first_issue/', owner, repo)

    if request_type == 'get':
        activity_rate = r.get(url_activity)
        help_wanted = r.get(url_help_wanted)
        good_first_issue = r.get(url_good_first_issue)
    elif request_type == 'post':
        activity_rate = r.post(url_activity)
        help_wanted = r.post(url_help_wanted)
        good_first_issue = r.post(url_good_first_issue)
    elif request_type == 'put':
        activity_rate = r.put(url_activity)
        help_wanted = r.put(url_help_wanted)
        good_first_issue = r.put(url_good_first_issue)

    metric = {
        'activity_rate': activity_rate['activity_rate'],
        'activity_rate_15_days': activity_rate['activity_rate_15_days'],
        'activity_rate_15_days_metric': activity_rate[
            'activity_rate_15_days_metric'],
        'total_issues': help_wanted['total_issues'],
        'help_wanted_issues': help_wanted['help_wanted_issues'],
        'good_first_issue': good_first_issue['good_first_issue'],
    }
    return metric


def get_url(url_app, owner, repo):
    return URL_ISSUE + url_app + owner + '/' + repo + '/'
