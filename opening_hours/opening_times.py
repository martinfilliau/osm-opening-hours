def check_time(time, value):
    """
    Check if the given time is inside the given value.
    Return True if it is, else False.
    """
    to_check = get_minutes_from_midnight(time)
    from_time, to_time = value.split('-')
    from_time = get_minutes_from_midnight(from_time)
    to_time = get_minutes_from_midnight(to_time)
    return from_time <= to_check <= to_time

def minutes_to_closing(time, value):
    """
    Return number of minutes to closing for given value.
    """
    pass

def get_minutes_from_midnight(value):
    """
    Return number of minutes from a hh:mm
    """
    hours, minutes = value.split(':')
    return int(hours)*60 + int(minutes)
