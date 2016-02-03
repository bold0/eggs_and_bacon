# coding: utf-8

import os
import re
from config import USE_ACCOUNTS_AS_RECIPIENTS


def get_subject():
    with open('subject.txt', 'r') as f:
        return f.read()


def get_content():
    with open('content.html', 'r') as f:
        return f.read()


def get_credentials():
    credentials = []
    for file in os.listdir(os.path.join(os.getcwd(), 'accounts')):
        _fp = os.path.join(os.getcwd(), 'accounts', file)
        smtp_server, port, ssl, starttls = file.split(' ')
        if ssl == 'ssl':
            ssl = True
        elif ssl == 'no_ssl':
            ssl = False

        if starttls == 'starttls':
            starttls = True
        elif starttls == ' no_starttls':
            starttls = False

        with open(_fp, 'r') as r:
            _data = r.readlines()
            for line in _data:
                try:
                    username, password = line.strip().split('\t')
                except:
                    continue
                credentials.append({'smtp_server': smtp_server,
                                    'port': port,
                                    'username': username,
                                    'password': password,
                                    'ssl': ssl,
                                    'starttls': starttls})
    return credentials


def get_recipients():
    recipients = []
    for file in os.listdir(os.path.join(os.getcwd(), 'recipients')):
        _fp = os.path.join(os.getcwd(), 'recipients', file)
        with open(_fp, 'r') as r:
            _data = r.readlines()
            for line in _data:
                _email = line.strip()
                if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", _email):
                    recipients.append(_email)

    if USE_ACCOUNTS_AS_RECIPIENTS:
        for acc in get_credentials():
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", acc.get('username')):
                recipients.append(acc.get('username'))
    return recipients


def get_attachments():
    files = []
    for file in os.listdir(os.path.join(os.getcwd(), 'attachments')):
        file_path = os.path.join(os.path.join(os.getcwd(), 'attachments'), file)
        files.append(file_path)
    return files
