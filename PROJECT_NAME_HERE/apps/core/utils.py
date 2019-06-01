import os
import time
from datetime import datetime

import requests
from django.conf import settings
from money import Money

from .models import Options

options = [
    ("site_title", "Letstream", "Site Title"),
    ("support_email", "support@theletstream.com", "Support Email"),
    ("site_description", "Site Developed by Letstream.", "Site Description"),
    ("smtp_server", "mail.example.com", "SMTP Server"),
    ("smtp_user", "admin", "SMTP User"),
    ("smtp_pass", "pass", "SMTP Pass"),
    ("smtp_port", "000", "SMTP Port"),
    ("send_mails_as", "admin@localhost", "Send Mails As"),
    ("site_url", "http://localhost:8000", "Site Url"),
    ('new_account_email_to_address', 'gsthealthcheckup@gmail.com',
     'New Account Email Notification To')
]


def addOption(key, value, label):
    try:
        option = Options.objects.create(key=key, value=value, label=label)
        return option
    except Exception:
        return False


def getOptions():
    try:
        site_options = Options.objects.all()
    except Exception as e:
        return None
    data = {}
    for x in site_options:
        data[x.key] = x.value
    return data


def getOption(key):
    try:
        option = Options.objects.get(key=key)
        return option.value
    except Options.DoesNotExist:
        return None


def setOption(key, value):
    try:
        option = Options.objects.get(key=key)
        option.value = value
        option.save()
        return True
    except Options.DoesNotExist:
        return False


def getEpochTimeSeconds(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt-epoch).total_seconds()


def lastIndexOf(list_obj, ele):
    return len(list_obj) - list_obj[::-1].index(ele) - 1


def create_temp_file(content, extension="noextension"):
    file_name = time.time()
    file_path = "%s/%s.%s" % (settings.TEMP_FILE_PATH, file_name, extension)
    with open(file_path, "wb") as f:
        f.write(content)

    return os.path.abspath(file_path)


def create_temp_file_from_url(url):
    try:
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            return create_temp_file(r.content)
        return None
    except Exception:
        raise


def format_currency(value):
    try:
        value = float(value)
    except Exception:
        raise
    m = Money(amount=value, currency="INR").format('en_IN')[2:]
    return m
