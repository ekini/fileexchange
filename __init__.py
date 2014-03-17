#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from gevent import monkey
#monkey.patch_socket()

from flask import Flask, render_template, flash, url_for, jsonify
from flask import request
from flask import redirect
from flaskext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = Flask(__name__)
#app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/base.db'
app.config['SECRET_LEY'] = 'dfgfdglfdgdfkgjfkjgefjr9tj49t tj49tj49tj'
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
db = SQLAlchemy(app)

babel = Babel(app)

#def format_datetime(value):
#    return unicode(value.strftime("%a, %d, %b %Y %H:%M"), "utf-8")
from flaskext.babel import format_datetime as format_datetime_babel


def format_datetime(value):
    return format_datetime_babel(value, 'EEEE, d MMMM yyyy H:mm')


def sizeof_fmt(num):
    num = float(num)
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


#import urllib
# well, seems like it doesn't need encoding
def urlquote(string):
    #return urllib.quote(string.encode("utf-8"))
    return string

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['filesize'] = sizeof_fmt
app.jinja_env.filters['urlquote'] = urlquote


def register_blueprints(app):
    # Prevents circular imports
    from fileexchange.user import user

    app.register_blueprint(user)

register_blueprints(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['ru', 'en'])

if __name__ == "__main__":
    pass
