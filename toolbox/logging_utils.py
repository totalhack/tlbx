from pprint import pformat
import sys

import sqlparse as sp

from toolbox.object_utils import get_class_vars

# TODO: allow use of python logging module?

class FontSpecialChars:
    ENDC = '\033[0m'

class FontColors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    NONE = '' # Will use default terminal coloring

RESERVED_COLORS = [
    'RED',    # errors
    'YELLOW', # warnings
    'BLACK',  # to avoid conflicts with terminal defaults
    'WHITE'   # to avoid conflicts with terminal defaults
]
COLOR_OPTIONS = [x for x in get_class_vars(FontColors) if x not in RESERVED_COLORS]

class FontEffects:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERTED = '\033[7m'

def sqlformat(sql):
    return sp.format(sql, reindent=True, keyword_case='upper')

def log(msg, label='parent', indent=0, color=None, autocolor=False, format_func=pformat):
    if isinstance(format_func, str):
        format_func = globals()[format_func]

    if format_func and format_func != pformat:
        msg = format_func(msg)
        if label:
            msg = '\n' + msg
    elif not isinstance(msg, str):
        msg = pformat(msg)
        if label:
            msg = '\n' + msg

    if indent is not None and int(indent):
        msg = (' ' * int(indent)) + msg

    if label:
        if label == 'parent':
            label = sys._getframe().f_back.f_code.co_name
        msg = label.strip() + ': ' + msg

    if (not color) and autocolor:
        assert label, 'No label provided, can not use autocolor'
        color_index = ord(label[0]) % len(COLOR_OPTIONS)
        color = COLOR_OPTIONS[color_index]

    if color:
        msg = getattr(FontColors, color.upper()) + msg + FontSpecialChars.ENDC

    print(msg)

def dbg(msg, label='parent', config=None, **kwargs):
    if config and not config.get('DEBUG', False):
        return

    if label == 'parent':
        label = sys._getframe().f_back.f_code.co_name
    log(msg, label=label, autocolor=True, **kwargs)

def dbgsql(sql, label='parent', config=None):
    if label == 'parent':
        label = sys._getframe().f_back.f_code.co_name

    dbg(sql, label=label, config=config, format_func=sqlformat)

def warn(msg, label='WARNING'):
    log(msg, label=label, color='yellow')

def error(msg, label='ERROR'):
    log(msg, label=label, color='red')

class PrintMixin:
    repr_attrs = []

    def __repr__(self):
        if self.repr_attrs:
            return "<%s %s>" % (type(self).__name__, ' '.join(['%s=%s' % (field, getattr(self, field))
                                                               for field in self.repr_attrs]))
        return "<%s %s>" % (type(self).__name__, id(self))

    def __str__(self):
        return str(vars(self))
