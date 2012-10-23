#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_socket()

from flask import Flask, render_template, flash, url_for, jsonify
from flask import request
from flask import redirect
#from flask_login import (LoginManager, login_required, login_user,
#                         logout_user, current_user)
from flask.ext.mongoengine import MongoEngine
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = "upload"

SECRET_KEY = "dfjewpr39fedffgfgfgf"

app = Flask(__name__)
app.config.from_object(__name__)

def format_datetime(value):
    return unicode(value.strftime("%a, %d, %b %Y %H:%M"), "utf-8")

def sizeof_fmt(num):
    num = float(num)
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['filesize'] = sizeof_fmt

# connect to the database
db = MongoEngine(app)


def register_blueprints(app):
    # Prevents circular imports
    from fileexchange.user import user

    app.register_blueprint(user)

register_blueprints(app)


if __name__ == "__main__":
    app.debug = True
#    app.run("0.0.0.0")
    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
