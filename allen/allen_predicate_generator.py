import datetime

def is_valid_date(date):
    try:
        valid_date = datetime.datetime.strptime(date, '%Y-%M-%d')
        return True
    except ValueError:
        return False

def is_before(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_end + ' < ' + range2_start)

def is_after(range1_start, range1_end, range2_start, range2_end):
    return is_before(range2_start, range2_end, range1_start, range1_end)

def is_equal(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' = ' + range2_start + ' AND ' + range1_end + ' = ' + range2_end)

def meet(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' < ' + range2_start + ' AND ' + range1_end + ' = ' + range2_start)

def is_met_by(range1_start, range1_end, range2_start, range2_end):
    return meet(range2_start, range2_end, range1_start, range1_end)

def overlap(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' < ' + range2_start + ' AND ' + range1_end + ' > ' + range2_start)

def is_overlapped_by(range1_start, range1_end, range2_start, range2_end):
    return overlap(range2_start, range2_end, range1_start, range1_end)

def is_during(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' >= ' + range2_start + ' AND ' + range1_end + ' <= ' + range2_end)

def contain(range1_start, range1_end, range2_start, range2_end):
    return is_during(range2_start, range2_end, range1_start, range1_end)

def start(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' = ' + range2_start + ' AND ' + range1_end + ' < ' + range2_end)

def is_started_by(range1_start, range1_end, range2_start, range2_end):
    return start(range2_start, range2_end, range1_start, range1_end)

def finish(range1_start, range1_end, range2_start, range2_end):
    if is_valid_date(range1_start):
        range1_start = '\'' + range1_start + '\''
    if is_valid_date(range1_end):
        range1_end = '\'' + range1_end + '\''
    if is_valid_date(range2_start):
        range2_start = '\'' + range2_start + '\''
    if is_valid_date(range2_end):
        range2_end = '\'' + range2_end + '\''

    return (range1_start + ' > ' + range2_start + ' AND ' + range1_end + ' = ' + range2_end)

def is_finished_by(range1_start, range1_end, range2_start, range2_end):
    return finish(range2_start, range2_end, range1_start, range1_end)
