from opening_hours.opening_times import is_open as is_open_time 

DAYS_OF_THE_WEEK = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

def is_open(day, time, value):
    if value == "24/7": return True

    definitions = value.split(';')
    opening_hours = {}
    for definition in definitions:
        # Mo-Fr 08:30-20:00
        d, r = definition.strip().split(' ')
        ranges = r.split(',')
        if '-' in d:
            day_from, day_to = d.split('-')
            day_fr = DAYS_OF_THE_WEEK.index(day_from)
            day_t = DAYS_OF_THE_WEEK.index(day_to)
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
    
    if not day in opening_hours: return False

    for op_hours in opening_hours[day]:
        if is_open_time(time, op_hours):
            return True
    return False
