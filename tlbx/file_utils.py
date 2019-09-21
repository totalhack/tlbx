import os
import subprocess


def rmfile(filename, ignore_missing=False):
    try:
        os.remove(filename)
    except FileNotFoundError:
        if ignore_missing:
            return
        raise


def shell(cmd, shell=True, capture_output=True, **kwargs):
    return subprocess.run(cmd, shell=shell, capture_output=capture_output, **kwargs)
