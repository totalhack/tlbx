from datetime import datetime
from dateutil import parser as dateparser, tz
from dateutil.zoneinfo import get_zonefile_instance


def parse_date(s):
    return dateparser.parse(s)


def get_tz_names():
    return list(get_zonefile_instance().zones)


def utcnow():
    dt = datetime.utcnow()
    utc_tz = tz.gettz("UTC")
    dt = dt.replace(tzinfo=utc_tz)
    return dt


def to_tz(dt, tz_name, strip_tz=False):
    to_tz = tz.gettz(tz_name)
    if not to_tz:
        raise Exception("Invalid timezone name: %s") % tz_name

    dt = dt.astimezone(to_tz)
    if strip_tz:
        return dt.replace(tzinfo=None)

    return dt
