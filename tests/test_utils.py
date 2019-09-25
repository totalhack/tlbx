import configparser
import logging
import os
import pytest

assert "TLBX_CONFIG" in os.environ, (
    "Please specify the location of a tlbx config file using the "
    "environment variable TLBX_CONFIG"
)

config = configparser.ConfigParser()
config.read(os.environ["TLBX_CONFIG"])
test_config = config["TEST"]

logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture(scope="function")
def print_one_line():
    print("\n")
    return None
