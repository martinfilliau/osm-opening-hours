def get_minutes_from_midnight(value):
    """
    Return number of minutes from a hh:mm
    """
    hours, minutes = value.split(':')
    return int(hours)*60 + int(minutes)


def clean_value(value):
    """
    Attempt to clean a value (value being an opening hours string)
    """
    value = value.lower().strip()
    if value.endswith(";"):
        value = value[0:-1]
    return value


class ParseException(Exception):

    def __init__(self, value_to_parse, inner_message):
        self.message = "Can't parse value: \"{0}\", {1}".format(value_to_parse.replace("\n", ""), inner_message)
        Exception.__init__(self, self.message)
