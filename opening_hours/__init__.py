from opening_hours.opening_times import is_open as is_open_time
from opening_hours.opening_times import minutes_to_closing

DAYS_OF_THE_WEEK = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']


class OpeningHours(object):

    def __init__(self, value):
        """
        @param value to parse
        """
        self.value = clean_value(value)
        self.is_always_open = False
        if self.value == "24/7":
            self.is_always_open = True
            return    # can't parse this value atm
        
        try:
            self.opening_hours = parse_string(self.value)
        except Exception, e:
            raise ParseException(value, e)

    def is_open(self, day, time):
        """
        Return True if open for given day and time, else False
        """
        if self.is_always_open: return True
        day = day.lower()

        if not day in self.opening_hours: return False

        for op_hours in self.opening_hours[day]:
            if is_open_time(time, op_hours):
                return True
        return False

    def minutes_to_closing(self, day, time):
        """
        Return 0 if closed for given day and time, else number of minutes to closing
        """
        if self.is_always_open: return -1   # TODO value for "not closing"?
        day = day.lower()

        if not day in self.opening_hours: return 0

        for op_hours in self.opening_hours[day]:
            minutes = minutes_to_closing(time, op_hours)
            if minutes > 0:
                return minutes
        return 0

    def get_as_dictionnary(self):
        """
        Get parsed value as a dict of day containing ranges of opened times
        """
        return self.opening_hours


def parse_string(value):
    """
    Parse a string in the OSM format
    Returns a dict with day of the week as key and
    a list of range of opening hours
    """
    opening_hours = {}
    for definition in value.split(';'):
        # Mo-Fr 08:30-20:00
        d, r = definition.strip().split(' ')
        ranges = r.split(',')
        if '-' in d:
            day_from, day_to = d.split('-')
            day_fr = DAYS_OF_THE_WEEK.index(day_from.lower())
            day_t = DAYS_OF_THE_WEEK.index(day_to.lower())
            for da in DAYS_OF_THE_WEEK[day_fr:day_t + 1]:
                for ra in ranges:
                    if da in opening_hours:
                        opening_hours[da].append(ra)
                    else:
                        opening_hours[da] = [ra]
        else:
            for ra in ranges:
                if d in opening_hours:
                    opening_hours[d].append(ra)
                else:
                    opening_hours[d] = [ra]
    return opening_hours


def clean_value(value):
    value = value.lower()
    if value.endswith(";"):
        value = value[0:-1]
    return value


class ParseException(Exception):

    def __init__(self, value_to_parse, inner_message):
        self.message = "Can't parse value: \"{0}\", {1}".format(value_to_parse.replace("\n", ""), inner_message)
        Exception.__init__(self, self.message)
