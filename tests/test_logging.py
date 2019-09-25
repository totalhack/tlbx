import logging
import random
import string

from .test_utils import *
from tlbx.logging_utils import *
from tlbx.object_utils import get_caller


my_logger = logging.getLogger(__name__)
my_logger.setLevel(logging.INFO)


def my_dbg(msg):
    dbg(msg, label=get_caller(), logger=my_logger)


def my_info(msg):
    info(msg, label=get_caller(), logger=my_logger)


def my_warn(msg):
    warn(msg, label=get_caller(), logger=my_logger)


def my_error(msg):
    error(msg, label=get_caller(), logger=my_logger)


def test_dbg():
    dbg("Test")


def test_info():
    info("Test")


def test_warn():
    warn("Test")


def test_error():
    error("Test")


def test_my_dbg():
    my_dbg("Test")


def test_my_info():
    my_info("Test")


def test_my_warn():
    my_warn("Test")


def test_my_error():
    my_error("Test")


def random_string(N):
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(N)
    )


INDENT_STRING = """Test indent sentence 1.
This is sentence 2"""
LONG_INDENT_STRING = """This is a longer sentence that would naturally wrap on its own. Let's see if the wrapping works.
This is a second sentence that is not quite as long.
"""
INDENT_OBJ = {
    "test": random_string(20),
    "test2": random_string(20),
    "test3": list(range(0, 25)),
    "test4": {
        "subtest1": random_string(10),
        "subtest2": 934593,
        "subtest3": list(range(0, 20)),
    },
}


def test_indent_int(print_one_line):
    dbg(INDENT_STRING, indent=4)


def test_indent_label(print_one_line):
    dbg(INDENT_STRING, indent="label")


def test_indent_no_label(print_one_line):
    dbg(INDENT_STRING, indent=4, label=None, autocolor=False)


def test_indent_long_by_int(print_one_line):
    dbg(LONG_INDENT_STRING, indent=4)


def test_indent_long_by_label(print_one_line):
    dbg(LONG_INDENT_STRING, indent="label")


def test_indent_long_no_label(print_one_line):
    dbg(LONG_INDENT_STRING, indent=4, label=None, autocolor=False)


def test_indent_int_obj(print_one_line):
    dbg(INDENT_OBJ, indent=4)


def test_indent_obj_no_label(print_one_line):
    dbg(INDENT_OBJ, indent=4, label=None, autocolor=False)


def test_indent_obj_label(print_one_line):
    dbg(INDENT_OBJ, indent="label")


def test_indent_obj_no_indent_or_label(print_one_line):
    dbg(INDENT_OBJ, indent=None, label=None, autocolor=False)


def test_repr_obj(print_one_line):
    dbg(INDENT_OBJ, indent=4, format_func="repr")
