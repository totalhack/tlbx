import pytest
from unittest.mock import patch

from .test_utils import *
from tlbx import Script, Arg


@Script(
    Arg("name", help="A name"),
    Arg("--flag", help="A flag", action="store_true", required=False, default=True),
)
def script(name, flag):
    print("Name:", name)
    print("Flag:", flag)


def test_run_script():
    with patch("argparse._sys.argv", ["test_script_decorator.py", "test"]):
        script()


def test_help():
    with patch("argparse._sys.argv", ["test_script_decorator.py", "--help"]):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            script()
