#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import url_for
from fileexchange import db
import datetime

class File(db.Document):
    name = db.StringField(max_length=255, required=True)
    path = db.StringField(max_length=1024, required=True)
    owner = db.StringField(max_length=255, required=True)
    type = db.StringField(max_length=255, required=True)
    md5 = db.StringField(max_length=255, required=True)
    size = db.IntField(required=True)
    count = db.IntField(required=True, default=0)
    uploaded = db.DateTimeField(default=datetime.datetime.now)
    savetime = db.DateTimeField(required=True)
    meta = {
        "indexes": ["owner", "path", "-uploaded"]
    }

