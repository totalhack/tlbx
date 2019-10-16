import io

from .test_utils import *
from tlbx.cli_utils import st
from tlbx.iterable_utils import *
from tlbx.logging_utils import info
from tlbx.string_utils import random_string


def test_read_chunks():
    text = ""
    for i in range(0, 20):
        text += random_string(10) + "\n"
    buf = io.StringIO(text)

    last_id = None
    for chunk in read_chunks(buf, 3, 14):
        info(chunk)
        if last_id:
            info("id:%s last:%s equal:%s" % (id(chunk), last_id, last_id == id(chunk)))
            assert last_id != id(chunk)
        last_id = id(chunk)
