import datetime
import logging
import os
import requests
import tempfile
from decouple import config, Csv


# Configuración de telegram (copiada en samaritano/settings.py)
BOT_URL = config("BOT_URL", default="https://api.telegram.org")
BOT_PREFIX = config('BOT_PREFIX', default="")
BOT_TOKEN = config('BOT_TOKEN', default="")
BOT_CHATIDS = config('BOT_CHATIDS', cast=Csv(), default="")
BOT_ENABLED = BOT_URL and BOT_PREFIX and BOT_TOKEN and BOT_CHATIDS


def _api_url(command):
    return "{}/bot{}/{}".format(BOT_URL, BOT_TOKEN, command)


def send_message(message):
    if not BOT_ENABLED:
        return
    url = _api_url("sendMessage")
    for chat_id in BOT_CHATIDS:
        json_data = {"chat_id": chat_id, "text": message, "parse_mode": 'HTML'}
        requests.post(url, json=json_data)


def send_document(message, filename):
    if not BOT_ENABLED:
        return
    url = _api_url("sendDocument")
    files = {'document': open(filename, "rb")}
    for chat_id in BOT_CHATIDS:
        json_data = {"chat_id": chat_id, "caption": message, "parse_mode": 'HTML'}
        requests.post(url, data=json_data, files=files)


def _request_format(request):
    def line(attr, value): return "{}: {}\n".format(attr.upper(), value)

    s = line('URI', request.build_absolute_uri())
    for attr in ['method', 'user']:
        s += line(attr, getattr(request, attr))
    for attr in ['REMOTE_ADDR', 'HTTP_REFERER']:
        s += line(attr, request.META.get(attr, "-"))
    s += line('DATE', datetime.datetime.now())
    return s


class TelegramHandler(logging.Handler):
    def emit(self, record):
        if hasattr(record, 'request'):
            exceptionname = record.exc_info[0].__name__ + "_" if record.exc_info else ""
            dirname = tempfile.mkdtemp()
            filename = "{}{}.txt".format(exceptionname, datetime.datetime.now().strftime("%y%m%d_%H%M%S"))
            fullname = os.path.join(dirname, filename)
            content = _request_format(record.request) + "\n" + self.format(record)
            open(fullname, "w").write(content)
            send_document(BOT_PREFIX + "\n" + record.request.build_absolute_uri(), fullname)
            os.unlink(fullname)
            os.rmdir(dirname)
        else:
            content = BOT_PREFIX + "\n" + self.format(record)
            send_message(content)
