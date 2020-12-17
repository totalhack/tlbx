import os
import subprocess
import sys
import time

pandas = None
try:
    import pandas
except ImportError:
    pass

if pandas:
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
    if sys.version_info.major == 3 and sys.version_info.minor >= 7:
        return subprocess.run(cmd, shell=shell, capture_output=capture_output, **kwargs)
    else:
        process = subprocess.Popen(
            cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return process.communicate()


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
    if not pandas:
        raise Exception("Please install pandas to use this function")

    f, _, compression, should_close = get_filepath_or_buffer(f, compression=compression)

    close = False or should_close
    if isinstance(f, str):
        close = True

    f, handles = get_handle(f, open_flags, compression=compression)

    return f, handles, close


def read_filepath_or_buffer(f, open_flags="r", compression=None):
    """Open and read files or buffers, local or remote"""
    f, handles, close = open_filepath_or_buffer(
        f, open_flags=open_flags, compression=compression
    )
    try:
        data = f.read()
    finally:
        if close:
            try:
                f.close()
            except ValueError:
                pass
    return data


def get_modified_time(fname):
    """Utility to get the modified time of a file"""
    return os.stat(fname).st_mtime


def get_time_since_modified(fname):
    """Utility to get the time since a file was last modified"""
    return time.time() - get_modified_time(fname)
