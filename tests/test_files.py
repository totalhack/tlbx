from .test_utils import *
from tlbx import st
from tlbx.file_utils import open_filepath_or_buffer, shell


def test_open_filepath_or_buffer():
    f, _, close = open_filepath_or_buffer("textfile.txt", open_flags="r")

    try:
        lines = f.read()
        print(lines)
    finally:
        if close:
            f.close()


def test_shell():
    out = shell("ls -lt /tmp", shell=True)
    assert out
