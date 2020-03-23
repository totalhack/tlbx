def raiseif(cond, msg="", exc=AssertionError):
    if cond:
        raise exc(msg)


def raiseifnot(cond, msg="", exc=AssertionError):
    raiseif(not cond, msg=msg, exc=exc)
