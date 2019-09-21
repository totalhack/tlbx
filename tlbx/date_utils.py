from dateutil import parser as dateparser


def parse_date(s):
    return dateparser.parse(s)
