import attr
from email import parser, policy
from email.message import EmailMessage
import logging
import mimetypes
import ntpath
import smtplib

from imapclient import IMAPClient

from tlbx.object_utils import MappingMixin

SMTP_SSL_PORT = 465

imapclient_logger = logging.getLogger("imapclient")
imapclient_logger.setLevel(logging.WARNING)


@attr.s(kw_only=True)
class EmailPayload(MappingMixin):
    payload = attr.ib()
    content_type = attr.ib()
    charset = attr.ib()


def update_email(
    msg, frm=None, to=None, subject=None, body=None, html=None, attachments=None
):
    if frm:
        msg.replace_header("from", frm)

    if to:
        msg.replace_header("to", to)

    if subject:
        msg.replace_header("subject", subject)

    if body:
        if msg.is_multipart():
            payload = msg.get_payload()
            new_body = EmailMessage()
            new_body.set_content(body)
            payload[0] = new_body
            msg.set_payload(payload)
        else:
            msg.set_content(body)

    if html:
        msg.add_alternative(html, subtype="html")

    if attachments:
        if msg.is_multipart():
            payload = msg.get_payload()
            # Try to only keep the body. There might be a better way
            msg.set_payload(payload[:1])
        add_email_attachments(attachment)

    return msg


# -------- Read Emails


def extract_email_payload(msg, decode=True):
    def decode_if_necessary(payload, charset):
        # decode=True still returns encoded bytes, but just decodes
        # the message contents from transfer encoding, such as if the
        # payload is base64 encoded.
        charset = charset or "utf8"  # Fall back to utf8
        if (not decode) or (not isinstance(payload, bytes)):
            return payload
        return payload.decode(charset)

    if msg.is_multipart():
        parts = []
        for part in msg.walk():
            if "multipart" in part.get_content_type().lower():
                continue
            charset = part.get_content_charset()
            payload = part.get_payload(decode=decode)
            payload = decode_if_necessary(payload, charset)
            parts.append(
                EmailPayload(
                    content_type=part.get_content_type(),
                    charset=charset,
                    payload=payload,
                )
            )
        return parts
    else:
        # When is_multipart is False, payload is a string
        charset = msg.get_content_charset()
        payload = msg.get_payload(decode=decode)
        payload = decode_if_necessary(payload, charset)
        return [
            EmailPayload(
                content_type=msg.get_content_type(), charset=charset, payload=payload
            )
        ]


def read_email(
    criteria,
    folder="INBOX",
    sort=None,
    limit=None,
    client=None,
    host=None,
    username=None,
    password=None,
    **kwargs
):
    results = []
    logout = False

    if not client:
        assert (
            host and username and password
        ), "Must pass host/username/password for IMAP connection"
        logout = True
        client = IMAPClient(host, **kwargs)
        client.login(username, password)

    try:
        select_info = client.select_folder(folder)
        if sort:
            messages = client.sort(sort, criteria=criteria)
        else:
            messages = client.search(criteria)

        if limit:
            messages = messages[:limit]

        for msg_id, msg_data in client.fetch(messages, ["RFC822"]).items():
            raw = msg_data[b"RFC822"].decode("utf8")
            msg = parser.Parser(policy=policy.default).parsestr(raw)
            results.append(msg)

    finally:
        if logout:
            client.logout()

    return results


# -------- Write Emails


def add_email_attachments(msg, attachments):
    for attachment in attachments or []:
        assert ntpath.isfile(attachment), "Email attachments must be valid file paths"
        filename = ntpath.basename(attachment)

        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        with open(attachment, "rb") as fp:
            msg.add_attachment(
                fp.read(), maintype=maintype, subtype=subtype, filename=filename
            )


def create_email(frm, to, subject, body=None, html=None, attachments=None):
    msg = EmailMessage()
    msg["From"] = frm
    msg["To"] = to if isinstance(to, str) else ", ".join(to)
    msg["Subject"] = subject
    msg.preamble = "You will not see this in a MIME-aware mail reader.\n"
    msg.set_content(body or "")

    if html is not None:
        msg.add_alternative(html, subtype="html")

    add_email_attachments(msg, attachments)
    return msg


def send_email(
    msg,
    client=None,
    host=None,
    port=None,
    username=None,
    password=None,
    smtp_class=smtplib.SMTP,
    debug=False,
):
    if client:
        client.send_message(msg)
        return

    assert (
        host and port and username and password
    ), "Must pass host/port/username/password for SMTP connection"

    if port == SMTP_SSL_PORT:
        smtp_class = smtplib.SMTP_SSL

    with smtp_class(host, port=port) as client:
        client.ehlo()
        if smtp_class == smtplib.SMTP:
            client.starttls()
            client.ehlo()
        client.login(username, password)
        client.set_debuglevel(debug)
        client.send_message(msg)
