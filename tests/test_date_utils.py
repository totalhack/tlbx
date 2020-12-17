from datetime import timedelta

from tlbx.date_utils import utcnow, to_tz


def test_tz_conversion():
    utc = utcnow()
    est = to_tz(utc, "US/Eastern", strip_tz=True)
    utc = utc.replace(tzinfo=None)
    assert (utc - est) in [timedelta(hours=5), timedelta(hours=4)]
