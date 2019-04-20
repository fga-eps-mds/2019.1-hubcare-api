from datetime import datetime, timezone


def date_check(tested_variable):
    '''
    verifies if the time difference between the last update and now is
    greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(tested_variable and (datetime_now - tested_variable[0].date).days >= 1):
        return True
    return False
