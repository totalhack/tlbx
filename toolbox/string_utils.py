import random
import string


def is_str(o):
    try:
        basestring
    except NameError:
        basestring = (str, bytes)
    return isinstance(o, basestring)


def is_int(v):
    if v is True or v is False:
        return False

    try:
        int(str(v))
        return True
    except ValueError:
        return False


def is_num(v):
    if v is True or v is False:
        return False

    try:
        float(v)
        return True
    except ValueError:
        return False


def get_string_format_args(s):
    return [tup[1] for tup in string.Formatter().parse(s) if tup[1] is not None]


def string_has_format_args(s):
    if get_string_format_args(s):
        return True
    return False


def random_string(length=10):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))
