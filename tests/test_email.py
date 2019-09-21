import datetime
import time

from .test_utils import *
from tlbx.logging_utils import dbg
from tlbx.email_utils import *


def test_read_email():
    criteria = ["SINCE", datetime.date.today().strftime("%d-%b-%Y")]
    msgs = read_email(
        criteria=criteria,
        limit=2,
        host=test_config["IMAPHost"],
        username=test_config["IMAPUsername"],
        password=test_config["IMAPPassword"],
    )
    for msg in msgs:
        dbg(msg)
        payload = extract_email_payload(msg)
        dbg(payload)


def test_send_email():
    msg = create_email(
        test_config["SMTPUsername"],
        test_config["EmailDestination"],
        subject="Test Send Email: %s" % time.time(),
        body="Test body",
        html="<p>Alternative HTML</p>",
        attachments=["textfile.txt"],  # TODO: use pkg_resource
    )
    send_email(
        msg,
        host=test_config["SMTPHost"],
        port=test_config["SMTPPort"],
        username=test_config["SMTPUsername"],
        password=test_config["SMTPPassword"],
    )
