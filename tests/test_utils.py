import configparser
import logging
import os

assert "TOOLBOX_CONFIG" in os.environ, (
    "Please specify the location of a toolbox config file using the "
    "environment variable TOOLBOX_CONFIG"
)

config = configparser.ConfigParser()
config.read(os.environ["TOOLBOX_CONFIG"])
test_config = config["TEST"]

logging.getLogger().setLevel(logging.DEBUG)
