import os
import subprocess

from pandas.io.common import get_filepath_or_buffer

try:
    from pandas.io.common import _get_handle as get_handle
except ImportError:
    from pandas.io.common import get_handle


def rmfile(filename, ignore_missing=False):
    try:
        os.remove(filename)
    except FileNotFoundError:
        if ignore_missing:
            return
        raise


def shell(cmd, shell=True, capture_output=True, **kwargs):
    return subprocess.run(cmd, shell=shell, capture_output=capture_output, **kwargs)


def open_filepath_or_buffer(f, open_flags="r", compression=None):
    """Use pandas IO functions to return a handle from a filepath
    or buffer.

    Parameters
    ----------
    f : str or buffer
        filepath or buffer to open
    open_flags : str, optional
        mode to open file
    compression : str, optional
        compression arg passed to pandas functions

    Returns
    -------
    f : file-like
        A file-like object
    handles : list of file-like
        A list of file-like objects opened. Seems mostly relevant for zipped archives.
    close : bool
        A flag indicating whether the caller should close the file object when done

    """
    f, _, compression, should_close = get_filepath_or_buffer(f, compression=compression)

    close = False or should_close
    if isinstance(f, str):
        close = True

    f, handles = get_handle(f, open_flags, compression=compression)

    return f, handles, close
