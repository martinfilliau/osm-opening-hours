from collections import defaultdict

from osm_time import ParseException, clean_value, get_minutes_from_midnight

# Days of the week + ph (public holiday)
DAYS_OF_THE_WEEK = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su', 'ph']


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
        except Exception as e:
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
        if '-' in d:
            day_from, day_to = d.split('-')
            day_fr = DAYS_OF_THE_WEEK.index(day_from.lower())
            day_t = DAYS_OF_THE_WEEK.index(day_to.lower())
            # Complete the dict for days between beginning and end
            # e.g. Mo-Th --> Mo,Tu,We,Th
            for da in DAYS_OF_THE_WEEK[day_fr:day_t + 1]:
                opening_hours[da] = process_ranges(r)
        else:
            opening_hours[d] = process_ranges(r)
    return opening_hours


def process_ranges(ranges):
    """
    Processes a list of time ranges, returns a list of tuples
    """
    values = list()
    for ra in ranges.split(','):
        if ra != "off":
            values.append(process_time_range(ra))
    return values


def process_time_range(value):
    """
    Return a tuple with (from, to) time in minutes from midnight.
    """
    from_time, to_time = value.split('-')
    from_t = get_minutes_from_midnight(from_time)
    to_t = get_minutes_from_midnight(to_time)
    return (from_t, to_t)
