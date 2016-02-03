# coding: utf-8
import os
import sys
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate


def connect_to_smtp_ssl(server, ssl, starttls, username, password, port=None):
    try:
        if not ssl:
            port = smtplib.SMTP_SSL_PORT if not port else port
            server_c = smtplib.SMTP(server, port)
            server_c.ehlo()
            if starttls:
                server_c.starttls()
            server_c.ehlo()
        else:
            port = smtplib.SMTP_SSL_PORT if not port else port
            server_c = smtplib.SMTP_SSL(server, port)
            server_c.ehlo()
            if sys.version_info[0:3] <= (2, 6, 0) or sys.version_info[0:3] == (2, 6, 2):
                server_c = smtplib.SMTP(server, port)
                server_c.ehlo()
                server_c.ehlo()
            else:
                server_c = smtplib.SMTP_SSL(server, port)
                server_c.ehlo()

            if starttls:
                server_c.starttls()
        server_c.login(username, password)
        return server_c

    except smtplib.SMTPAuthenticationError:
        print('authentication failure: {0}'.format(username))
        return False
    except smtplib.SMTPServerDisconnected:
        print('Connection unexpectedly closed: {0}'.format(username))
        return False


def send_mail(server, send_from, send_to, subject, text, attachments=[], html=False,
              charset='utf-8'):
    ret_val = False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "%s" % Header(subject, 'utf-8')
        msg['To'] = COMMASPACE.join(send_to)
        msg['From'] = send_from
        msg['Date'] = formatdate(localtime=True)

        msg.preamble = "This is a multi-part message in MIME format."

        if html:
            msg.attach(MIMEText(text, 'html'))
        else:
            msg.attach(MIMEText(text, _charset=charset))

        for file in attachments:
            if html:
                part = MIMEBase('image', 'jpg')
            else:
                part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            if html:
                part.add_header('Content-ID', "<%s>" % os.path.basename(file))
            msg.attach(part)

        server.sendmail(send_from, send_to, msg.as_string())
        ret_val = True

    except Exception as e:
        print(e)

    return ret_val
