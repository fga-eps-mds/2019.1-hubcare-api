'''
File to contain all formulas that
estimate each given score.
'''

def commit_score(commit_qtd):
    """
    Receive a number of commits
    Returns a number between 0 and 1

    Follows a linear distribution from 0
    to 10 commits;
    """
    if commit_qtd > 9:
        return 1
    
    return commit_qtd * 0.1;


def contributors_score(contributors_qtd):
    """
    Receive a number of contributors
    Returns a number between 0 and 1

    Follows a linear distribution from 0
    to 4 contributors;
    """
    if contributors_qtd > 3:
        return 1

    return contributors_qtd * 0.25;
