import logging

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
