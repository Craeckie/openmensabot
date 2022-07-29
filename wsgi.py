#! python3
# Inspired by https://youtu.be/ufaOgM9QYk0

# Openshift 3 Flask app
# In production environment you can use gunicorn --threads 8 wsgi:application

import os
from flask import Flask, request, redirect
application = Flask(__name__)

# TODO your host name here
PUBLIC_URL = os.getenv(
    'PUBLIC_URL',
    'https://123.starter-us-east.openshiftapps.com')
# TODO your postgres database
POSTGRES_URL = os.getenv(
    'POSTGRES_URL',
    'postgres://user:password@hostname.example.com:1234/databasename')
# TODO Cache storage location, persistent or temporary
OPENSHIFT_DATA_DIR = os.getenv("OPENSHIFT_DATA_DIR", "./data")
# TODO Google API key for https://maps.googleapis.com/maps/api/staticmap
GOOGLEAPI_KEY = os.getenv('GOOGLEAPI_KEY', '123456789abcdefghj123456789')
# TODO Google client key for signing urls
GOOGLEAPI_CLIENT_SECRET = os.getenv(
    'GOOGLEAPI_CLIENT_SECRET',
    '123456789abcdef_68ifgf=')
# TODO Insert your Telegram Token from @BotFather
TELEGRAM_TOKEN = os.getenv(
    'TELEGRAM_TOKEN',
    '710871591:AAAqqqIIIcccYYYAAA222WWWvvvfffqqq777k')
# TODO Insert your personal Telegram account id here
TELEGRAM_ADMIN = int(os.getenv(
    'TELEGRAM_ADMIN',
    0))

#if __name__ == "__main__":
#    # For local testing:
#    # Start ngrok server to get a public hostname. See:
#    # https://ngrok.com/download
#    print("Starting ngrok")
#    import ngrok
#    ngrok.start()
#    import time
#    print("Wait for ngrok . . . ")
#    time.sleep(3)
#    PUBLIC_URL = ngrok.getUrl()


print("Starting mensabot.Bot")
import mensabot
mensaCacheFile = os.path.join(OPENSHIFT_DATA_DIR, "mensacache.pickle")
myMensaBot = mensabot.Bot(
    telegramToken=TELEGRAM_TOKEN,
    mensaCacheFile=mensaCacheFile,
    postgresUrl=POSTGRES_URL,
    googleapi={
        "api_key": GOOGLEAPI_KEY,
        "client_secret": GOOGLEAPI_CLIENT_SECRET},
    admin=TELEGRAM_ADMIN)
myMensaBotWebHook = myMensaBot.run(PUBLIC_URL + "/telegramWebhook")
myMensaBot.worker()
print("mensabot.Bot is running")


@application.route("/")
def hello():
    try:
        return myMensaBot.status
    except BaseException:
        return "Hello World!"


@application.route("/favicon.ico")
def favicon():
    return redirect("https://www.openshift.com/favicon.ico", code=301)


@application.route("/health")
def health():
    return "OK"


@application.route("/probe_readiness")
def probe_readiness():
    if "Running" in myMensaBot.status:
        return "OK", 200
    else:
        return "Bots are not running", 503


@application.route("/probe_liveness")
def probe_liveness():
    return "OK"


@application.route("/telegramWebhook", methods=['GET', 'POST'])
def myMensaBotIncoming():
    myMensaBotWebHook.feed(request.data)
    return 'OK'


if __name__ == "__main__":
    application.run(host='127.0.0.1', port=8080, threaded=True)
