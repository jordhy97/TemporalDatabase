import datetime

def before(x, y):
    return (x.valid_from < y.valid_from
            and x.valid_from < y.valid_to
            and x.valid_to < y.valid_from
            and x.valid_to < y.valid_to)

def after(x, y):
    return before(y, x)

def equals(x, y):
    return (x.valid_from == y.valid_from
        and x.valid_from < y.valid_to
        and x.valid_to > y.valid_from
        and x.valid_to == y.valid_to)

def meets(x, y):
    return (x.valid_from < y.valid_from
        and x.valid_from < y.valid_to
        and x.valid_to == y.valid_from
        and x.valid_to < y.valid_to)

def met_by(x, y):
    return meets(y, x)

def overlaps(x, y):
    return (x.valid_from <= y.valid_from
        and x.valid_from < y.valid_to
        and x.valid_to > y.valid_from
        and x.valid_to <= y.valid_to)

def overlapped_by(x, y):
    return overlaps(y, x)

def during(x, y):
    return (x.valid_from >= y.valid_from
            and x.valid_from < y.valid_to
            and x.valid_to > y.valid_from
            and x.valid_to <= y.valid_to)

def contains(x, y):
    return during(y, x)

def starts(x, y):
    return (x.valid_from == y.valid_from
        and x.valid_from < y.valid_to
        and x.valid_to > y.valid_from
        and x.valid_to < y.valid_to)

def started_by(x, y):
    return starts(y, x)

def finishes(x, y):
    return (x.valid_from > y.valid_from
        and x.valid_from < y.valid_to
        and x.valid_to > y.valid_from
        and x.valid_to == y.valid_to)

def finished_by(x, y):
    return finishes(y, x)