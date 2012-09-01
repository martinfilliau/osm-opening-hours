from collections import defaultdict

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
            if op_hours[0] < get_minutes_from_midnight(time) < op_hours[1]:
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
            if op_hours[0] < get_minutes_from_midnight(time) < op_hours[1]:
                return op_hours[1] - get_minutes_from_midnight(time)
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
    opening_hours = defaultdict(list)
    for definition in value.split(';'):
        # Mo-Fr 08:30-20:00
        d, r = definition.strip().split(' ')
        ranges = r.split(',')
        if '-' in d:
            day_from, day_to = d.split('-')
            day_fr = DAYS_OF_THE_WEEK.index(day_from.lower())
            day_t = DAYS_OF_THE_WEEK.index(day_to.lower())
            # Complete the dict for days between beginning and end
            # e.g. Mo-Th --> Mo,Tu,We,Th
            for da in DAYS_OF_THE_WEEK[day_fr:day_t + 1]:
                for ra in ranges:
                    if ra != "off":
                        opening_hours[da].append(process_time_range(ra))
        else:
            for ra in ranges:
                if ra != "off":
                    opening_hours[d].append(process_time_range(ra))
    return opening_hours


def process_time_range(value):
    """
    Return a tuple with (from, to) time in minutes from midnight.
    """
    from_time, to_time = value.split('-')
    from_t = get_minutes_from_midnight(from_time)
    to_t = get_minutes_from_midnight(to_time)
    return (from_t, to_t)


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
