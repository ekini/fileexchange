#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from . import db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, DateTime, Enum, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship, sessionmaker


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    md5 = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    deletion_date = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    downloads = db.relationship("Log", order_by="Log.id", backref="file")

    def __repr__(self):
        return "<File('%r','%r')>" % (self.name, self.owner)

class Log(db.Model):
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    ip = db.Column(db.String, nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))

    def __init__(self, ip, file):
        self.ip = ip
        self.date = datetime.now()
        self.file_id = file.id

    def __repr__(self):
        return "<Log('%r','%r')>" % (self.date, self.ip, self.file.name)


