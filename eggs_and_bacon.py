# coding: utf-8

import random
import smtplib
import time

from multiprocessing import Pool, Queue
from config import PROCESSES, HOW_MANY_LOGINS, SEND_LIMIT_PER_USER

import easysmtp

from util import get_subject, get_content, get_recipients, get_credentials, get_attachments


class EggAndBacon:
    def __init__(self, **kwargs):
        self.attachments = kwargs.get('attachments')
        self.smtp_server = kwargs.get('smtp_server')
        self.port = kwargs.get('port')
        self.ssl = kwargs.get('ssl')
        self.recipients = kwargs.get('recipients')
        self.subject = kwargs.get('subject')
        self.content = kwargs.get('content')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.smtp_server = kwargs.get('smtp_server')
        self.starttls = kwargs.get('starttls')

    def smtp(self):
        return easysmtp.connect_to_smtp_ssl(self.smtp_server, self.ssl, self.starttls, self.username, self.password,
                                            self.port)

    def send_mail(self, smtp, recipient):
        try:
            easysmtp.send_mail(smtp, self.username, [recipient], self.subject, self.content, self.attachments,
                               html=True)
            print('email sent from ' + self.username + ' to ' + recipient)
        except smtplib.SMTPServerDisconnected as e:
            print(e)
            return False


def worker(work_queue):
    while True:
        eggz = work_queue.get()
        print('Analyzing ' + eggz.get('username'))
        c = EggAndBacon(**eggz)
        smtp = c.smtp()
        if not smtp:
            print('Cant connect to {0}'.format(eggz.get('username')))
            continue
        random_recipients = []
        all_recipients = eggz.get('recipients')
        for i in range(0, SEND_LIMIT_PER_USER):
            random_recipients.append(random.choice(all_recipients))
        for recipient in random_recipients:
            c.send_mail(smtp, recipient)
        smtp.close()


if __name__ == "__main__":
    queue = Queue()
    pool = Pool(PROCESSES, worker, (queue,))
    credentials = get_credentials()
    subject = get_subject()
    content = get_content()
    recipients = get_recipients()
    attachments = get_attachments()

    for x in range(0, HOW_MANY_LOGINS):
        credential = random.choice(credentials)
        args = {'smtp_server': credential.get('smtp_server'),
                'port': credential.get('port'),
                'username': credential.get('username'),
                'password': credential.get('password'),
                'ssl': credential.get('ssl'),
                'starttls': credential.get('starttls'),
                'subject': subject,
                'content': content,
                'recipients': recipients,
                'attachments': attachments}
        queue.put(args)
    
    time.sleep(5)
    while not queue.empty():
        time.sleep(1)
