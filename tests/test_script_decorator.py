from unittest.mock import patch

from .test_utils import *
from tlbx import Script, Arg


@Script(Arg("name", help="A name"))
def script(name):
    print("Name:", name)


def test_script():
    with patch("argparse._sys.argv", ["test_script_decorator.py", "test"]):
        script()
