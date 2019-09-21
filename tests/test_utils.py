import configparser
import logging
import os

assert "TLBX_CONFIG" in os.environ, (
    "Please specify the location of a tlbx config file using the "
    "environment variable TLBX_CONFIG"
)

config = configparser.ConfigParser()
config.read(os.environ["TLBX_CONFIG"])
test_config = config["TEST"]

logging.getLogger().setLevel(logging.DEBUG)
