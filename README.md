# telegram\_notify2

Django application for sending messages and error logging to telegram channel via bot

Requirements: requests, python-decouple, django >= 3


## Installation

Copy telegram.py to yourapplication folder (next to settings.py)

Insert the following lines in your settings.py:

```
# Telegram settings (the same in yourapplication/telegram.py)
BOT_URL = config("BOT_URL", default="https://api.telegram.org")
BOT_PREFIX = config('BOT_PREFIX', default="")
BOT_TOKEN = config('BOT_TOKEN', default="")
BOT_CHATIDS = config('BOT_CHATIDS', cast=Csv(), default="")
BOT_ENABLED = BOT_URL and BOT_PREFIX and BOT_TOKEN and BOT_CHATIDS

# Logging settings
from django.utils.log import DEFAULT_LOGGING
LOGGING = DEFAULT_LOGGING.copy()
# ...
if BOT_ENABLED:
    LOGGING['handlers']['telegram'] = {'level': 'ERROR', 'class': 'yourapplication.telegram.TelegramHandler'}
    LOGGING['loggers']['django']['handlers'].append('telegram')
    # LOGGING['loggers']['']['handlers'].append('telegram')
```

## Configuration

Required: Talk to @botfather and create a new bot, give it a name, and save http api key in the file `.env` this way:
```
BOT_TOKEN = "uid:hash_by_botfather"
```

Required: Prefix for messages
```
BOT_PREFIX= "[yourprefix]"
```

Required: Get the chatid(s) of the user or group or channel you want to talk. And add to `.env` this way:
```
BOT_CHATIDS = "chatid1,chatid2,..."
```

Not needed: Add to `.env` if you want to send messages to another api
```
BOT_URL = "https://api.telegram.org"  # default value
```


## Using

If you want to send a message, do the following:

```
from yourapplication.telegram import send_message
send_message("A useful message")
```

If you want to send a document, do the following:

```
from yourapplication.telegram import send_document
send_document("Caption", filename)
```

## Useful

In nginx use the following to pass remote hostname and client ip address:

```
location / {
	proxy_pass http://localhost:8000/;
	proxy_set_header Host            $host;
	proxy_set_header X-Real-IP       $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
