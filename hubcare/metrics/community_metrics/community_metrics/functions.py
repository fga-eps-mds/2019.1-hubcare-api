from datetime import datetime, timezone


def check_date(date_time):
    '''
    verifies if the time difference between
    the last update and now is greater than 24 hours
    '''
    datetime_now = datetime.now(timezone.utc)
    if(date_time and (datetime_now - date_time[0].date_time).days >= 1):
        return True
    return False


def serialized_object(object_serializer, object_for_filter_s):
    '''
    serialization of objects
    '''
    serializer_objects = object_serializer(
            object_for_filter_s
        )
    return serializer_objects
