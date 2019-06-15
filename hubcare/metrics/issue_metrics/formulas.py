'''
File to contain all formulas that
estimate each given score.
'''


def issue_activity_score(active_issues, open_issues):
    """
    Receive two numbers:
        number of active issues
        number of open issues

    Returns a number between 0 and 1

    Calcs a rate = active/open and
    follows a linear distribution of rate from
    0 to 0.75;
    """

    rate = active_issues / open_issues

    if rate >= 0.75:
        return 1

    return rate / 0.75


def good_first_issue_score(labeled_issues, total_issues):
    """
    Receive two numbers:
        number of open issues labeled with "good first issue"
        number of total open issues

    Returns a number between 0 and 1

    Calcs a rate = labeled/total and
    follows a linear distribution of rate from
    0 to 0.04;
    """

    rate = labeled_issues / total_issues

    if rate >= 0.04:
        return 1

    return labeled_issues / 0.04


def help_wanted_score(labeled_issues, total_issues):
    """
    Receive two numbers:
        number of open issues labeled with "help wanted"
        number of total open issues

    Returns a number between 0 and 1

    Calcs a rate = labeled/total and
    follows a linear distribution of rate from
    0 to 0.04;
    """

    rate = labeled_issues / total_issues

    if rate >= 0.04:
        return 1

    return labeled_issues / 0.04
