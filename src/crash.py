# Import smtplib for the actual sending function
# Import the email modules we'll need
import os
import smtplib as smtp
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

ADMIN_EMAIL = "1alekseik1@gmail.com"
OWN_EMAIL = "alekseik1@yandex.ru"


def send_crash_email(dump_dict: dict):
    msg = MIMEMultipart()
    msg["From"] = OWN_EMAIL
    msg["To"] = ADMIN_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = f"CRASH DUMP"

    msg.attach(
        MIMEText(
            "\n\n".join([dump_dict.get(key, ["None"])[0] for key in dump_dict.keys()])
        )
    )

    for key in dump_dict.keys():
        data = dump_dict[key][1]
        file_name = f"{key}.html"
        part = MIMEApplication(data, Name=file_name)
        part["Content-Disposition"] = 'attachment; filename="%s"' % file_name
        msg.attach(part)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtp.SMTP_SSL("smtp.yandex.com")
    server.set_debuglevel(1)
    server.ehlo(ADMIN_EMAIL)
    server.login(OWN_EMAIL, os.environ.get("YANDEX_PASSWORD"))
    server.auth_plain()
    server.sendmail(OWN_EMAIL, OWN_EMAIL, msg.as_string())
