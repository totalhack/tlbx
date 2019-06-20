import random
import string

def is_int(v):
    if v is True or v is False:
        return False

    try:
        i = int(str(v))
        return True
    except:
        return False

def is_num(v):
    if v is True or v is False:
        return False

    try:
        n = float(v)
        return True
    except:
        return False

def get_string_format_args(s):
    return [tup[1] for tup in string.Formatter().parse(s) if tup[1] is not None]

def string_has_format_args(s):
    if get_string_format_args(s):
        return True
    return False

def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
