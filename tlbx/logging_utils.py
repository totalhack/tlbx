import logging
from pprint import pformat, pprint as pp
import sys

import sqlparse as sp

from tlbx.object_utils import get_class_vars


class FontSpecialChars:
    ENDC = "\033[0m"


class FontColors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    NONE = ""  # Will use default terminal coloring


RESERVED_COLORS = [
    "RED",  # errors
    "YELLOW",  # warnings
    "BLACK",  # to avoid conflicts with terminal defaults
    "WHITE",  # to avoid conflicts with terminal defaults
]

COLOR_OPTIONS = [x for x in get_class_vars(FontColors) if x not in RESERVED_COLORS]


class FontEffects:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    INVERTED = "\033[7m"


logging.basicConfig(format="%(message)s")


def get_logging_level():
    return logging.getLogger().getEffectiveLevel()


def sqlformat(sql):
    return sp.format(sql, reindent=True, keyword_case="upper")


def format_msg(
    msg, label="parent", indent=0, color=None, autocolor=False, format_func=pformat
):
    if isinstance(format_func, str):
        format_func = globals()[format_func]

    if format_func and format_func != pformat:
        msg = format_func(msg)
        if label:
            msg = "\n" + msg
    elif not isinstance(msg, str):
        msg = pformat(msg)
        if label:
            msg = "\n" + msg

    if indent is not None and int(indent):
        msg = (" " * int(indent)) + msg

    if label:
        if label == "parent":
            label = sys._getframe().f_back.f_code.co_name
        msg = label.strip() + ": " + msg

    if (not color) and autocolor:
        assert label, "No label provided, can not use autocolor"
        color_index = ord(label[0]) % len(COLOR_OPTIONS)
        color = COLOR_OPTIONS[color_index]

    if color:
        msg = getattr(FontColors, color.upper()) + msg + FontSpecialChars.ENDC

    return msg


def log(msg, label="parent", **kwargs):
    if get_logging_level() > logging.INFO:
        return
    if label == "parent":
        label = sys._getframe().f_back.f_code.co_name
    msg = format_msg(msg, label=label, autocolor=True, **kwargs)
    logging.info(msg)


def dbg(msg, label="parent", **kwargs):
    if get_logging_level() > logging.DEBUG:
        return
    if label == "parent":
        label = sys._getframe().f_back.f_code.co_name
    msg = format_msg(msg, label=label, autocolor=True, **kwargs)
    logging.debug(msg)


def dbgsql(msg, label="parent", **kwargs):
    if get_logging_level() > logging.DEBUG:
        return
    if label == "parent":
        label = sys._getframe().f_back.f_code.co_name
    msg = format_msg(msg, label=label, autocolor=True, format_func=sqlformat, **kwargs)
    logging.debug(msg)


def warn(msg, label="parent", **kwargs):
    if get_logging_level() > logging.WARNING:
        return
    if label == "parent":
        label = sys._getframe().f_back.f_code.co_name
    msg = format_msg(msg, label=label, color="yellow", **kwargs)
    logging.warning(msg)


def error(msg, label="parent", **kwargs):
    if get_logging_level() > logging.ERROR:
        return
    if label == "parent":
        label = sys._getframe().f_back.f_code.co_name
    msg = format_msg(msg, label=label, color="red", **kwargs)
    logging.error(msg)


class PrintMixin:
    repr_attrs = []

    def __repr__(self):
        if self.repr_attrs:
            return "<%s %s>" % (
                type(self).__name__,
                " ".join(
                    [
                        "%s=%s" % (field, getattr(self, field))
                        for field in self.repr_attrs
                    ]
                ),
            )
        return "<%s %s>" % (type(self).__name__, id(self))

    def __str__(self):
        return str(vars(self))
