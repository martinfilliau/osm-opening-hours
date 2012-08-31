def is_open(time, value):
    """
    Check if the given time is inside the given value.
    Return True if it is, else False.
    """
    if value == "off": return False
    to_check = get_minutes_from_midnight(time)
    from_time, to_time = value.split('-')
    from_time = get_minutes_from_midnight(from_time)
    to_time = get_minutes_from_midnight(to_time)
    return from_time <= to_check <= to_time

def minutes_to_closing(time, value):
    """
    Return number of minutes to closing for given value, zero if it's closed.
    """
    # TODO DRY
    if value == "off": return 0
    to_check = get_minutes_from_midnight(time)
    from_time, to_time = value.split('-')
    from_time = get_minutes_from_midnight(from_time)
    to_time = get_minutes_from_midnight(to_time)
    if from_time <= to_check <= to_time:
        return to_time - to_check
    else:
        return 0

def get_minutes_from_midnight(value):
    """
    Return number of minutes from a hh:mm
    """
    hours, minutes = value.split(':')
    return int(hours)*60 + int(minutes)
