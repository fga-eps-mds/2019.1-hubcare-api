'''
File to contain all formulas that
estimate each given score.
'''


def pull_request_score(updated, merged):
    '''
    Receives:
        a list of Pull Request dicts (from github API)
        a list of merged PR dicts (from github API)
    Returns a dict with the following values:
        'acceptance_quality': number between 0 and 1, score;
        'categories': the number of PRs in each category

    The score is a mean of the score of all individual PRs
    ------------------------------------------------------
    Situation                 | Discussion  | Indv Score
    ------------------------------------------------------
    Merged                    | Yes	        | 1
    Merged	                  | No	        | 0.9
    Open                      | (<=15 days) | 0.9
    Closed and without merged | Yes         | 0.7
    Open	                  | (>15 days)	| 0.3
    Closed and without merged | No	        | 0.1
    Open                      | No/old      | 0
    -------------------------------------------------------
    '''

    pr_number = 0
    total_score = 0
    merged_pos = 0
    merged_size = len(merged)
    categories = {
        'merged_yes': 0,
        'merged_no': 0,
        'open_yes_new': 0,
        'closed_yes': 0,
        'open_yes_old': 0,
        'closed_no': 0,
        'open_no_old': 0
    }

    for i in updated:
        if pr_number >= TOTAL_PR:
            break
        elif merged_pos < merged_size and i['id'] == merged[merged_pos]['id']:
            if i['comments'] > 0:
                total_score += 1
                categories['merged_yes'] += 1
            else:
                total_score += 0.9
                categories['merged_no'] += 1
            merged_pos += 1
        elif i['state'] == 'closed':
            if i['comments'] > 0:
                total_score += 0.7
                categories['closed_yes'] += 1
            else:
                total_score += 0.1
                categories['closed_no'] += 1
        elif i['comments'] > 0:
            if check_datetime(i['updated_at']):
                total_score += 0.9
                categories['open_yes_new'] += 1
            else:
                total_score += 0.3
                categories['open_yes_old'] += 1
        else:
            categories['open_no_old'] += 1
        pr_number += 1

    if pr_number == 0:
        acceptance_quality = 0
    else:
        acceptance_quality = (total_score/pr_number)

    response = {
        'acceptance_quality': acceptance_quality,
        'categories': categories
    }
    return response