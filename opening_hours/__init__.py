from opening_hours.opening_times import is_open as is_open_time 

DAYS_OF_THE_WEEK = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']

def is_open(day, time, value):
    if value == "24/7": return True

    opening_hours = parse_string(value.lower())

    day = day.lower()

    if not day in opening_hours: return False

    for op_hours in opening_hours[day]:
        if is_open_time(time, op_hours):
            return True
    return False

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
            for da in DAYS_OF_THE_WEEK[day_fr:day_t+1]:
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
