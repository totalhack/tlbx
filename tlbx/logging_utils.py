import logging
from pprintpp import pformat as pf, pprint as pp
from reprlib import Repr
import shutil
import sys
from textwrap import indent, wrap

import sqlparse as sp

from tlbx.object_utils import get_class_vars, get_caller


logging.basicConfig(format="%(message)s")


_repr = Repr()
_repr.maxstring = 60
_repr.maxother = 20
_repr.maxlist = 5
_repr.maxtuple = 5
_repr.maxset = 5
repr = _repr.repr


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
    "NONE",  # to avoid conflicts with terminal defaults
]

COLOR_OPTIONS = sorted(
    [x for x in get_class_vars(FontColors) if x not in RESERVED_COLORS]
)


class FontEffects:
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    INVERTED = "\033[7m"


def get_terminal_width():
    return shutil.get_terminal_size().columns


def get_logging_level(logger=None):
    if (not logger) or (not isinstance(logger, logging.Logger)):
        logger = logging.getLogger()
    return logger.getEffectiveLevel()


def sqlformat(sql):
    return sp.format(sql, reindent=True, keyword_case="upper")


def format_msg(
    msg, label="parent", indent=None, color=None, autocolor=False, format_func=pf
):
    term_width = get_terminal_width()
    effective_width = term_width

    if label == "parent":
        label = get_caller()

    if indent is not None:
        if indent == "label":
            assert label, "indent=label but no label given"
            indent_str = " " * (len(label) + 2)
        else:
            indent = int(indent)
            indent_str = " " * indent
        effective_width = effective_width - len(indent_str)

    if isinstance(format_func, str):
        format_func = globals()[format_func]

    if format_func and format_func != pf:
        msg = format_func(msg)
        if label and not indent:
            msg = "\n" + msg
    elif not isinstance(msg, str):
        msg = pf(msg, width=effective_width)
        if label and not indent:
            msg = "\n" + msg

    if indent is not None:
        lines = msg.splitlines(True)
        msg = "\n".join(["\n".join(wrap(line, effective_width)) for line in lines])
        if indent == "label":
            msg = indent_str.join(msg.splitlines(True))
        else:
            msg = indent_str + indent_str.join(msg.splitlines(True))
            if label:
                msg = "\n" + msg

    if label:
        msg = label.strip() + ": " + msg

    if (not color) and autocolor:
        assert label, "No label provided, can not use autocolor"
        color_index = ord(label[0]) % len(COLOR_OPTIONS)
        color = COLOR_OPTIONS[color_index]

    if color:
        msg = getattr(FontColors, color.upper()) + msg + FontSpecialChars.ENDC

    return msg


def info(msg, label="parent", logger=None, autocolor=True, **kwargs):
    logger = logger or logging
    if get_logging_level(logger) > logging.INFO:
        return
    if label == "parent":
        label = get_caller()
    msg = format_msg(msg, label=label, autocolor=autocolor, **kwargs)
    logger.info(msg)


def dbg(msg, label="parent", logger=None, autocolor=True, **kwargs):
    logger = logger or logging
    if get_logging_level(logger) > logging.DEBUG:
        return
    if label == "parent":
        label = get_caller()
    msg = format_msg(msg, label=label, autocolor=autocolor, **kwargs)
    logger.debug(msg)


def dbgsql(msg, label="parent", logger=None, autocolor=True, **kwargs):
    logger = logger or logging
    if get_logging_level(logger) > logging.DEBUG:
        return
    if label == "parent":
        label = get_caller()
    msg = format_msg(
        msg, label=label, autocolor=autocolor, format_func=sqlformat, **kwargs
    )
    logger.debug(msg)


def warn(msg, label="parent", logger=None, **kwargs):
    logger = logger or logging
    if get_logging_level(logger) > logging.WARNING:
        return
    if label == "parent":
        label = get_caller()
    msg = format_msg(msg, label=label, color="yellow", **kwargs)
    logger.warning(msg)


def error(msg, label="parent", logger=None, **kwargs):
    logger = logger or logging
    if get_logging_level(logger) > logging.ERROR:
        return
    if label == "parent":
        label = get_caller()
    msg = format_msg(msg, label=label, color="red", **kwargs)
    logger.error(msg)


class PrintMixin:
    repr_attrs = []

    def __repr__(self):
        if self.repr_attrs:
            return "<%s %s>" % (
                type(self).__name__,
                " ".join(
                    [
                        "%s=%s" % (field, repr(getattr(self, field)))
                        for field in self.repr_attrs
                    ]
                ),
            )
        return "<%s %s>" % (type(self).__name__, id(self))

    def __str__(self):
        return str(pf(vars(self)))
