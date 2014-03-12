#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, DateTime, Enum, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship, sessionmaker

DATABASE = "sqlite:///base.db"
SQL_DEBUG = False

Base = declarative_base()

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    type = Column(String, nullable=False)
    md5 = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, nullable=False)
    deletion_date = Column(DateTime, nullable=False)
    deleted = Column(Boolean, default=False)
    downloads = relationship("Log", order_by="Log.id", backref="file")

    def __repr__(self):
        return "<File('%r','%r')>" % (self.name, self.owner)

class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    ip = Column(String, nullable=False)

    file_id = Column(Integer, ForeignKey('files.id'))
    #file = relationship("File", backref=backref('log', order_by=id))

    def __init__(self, ip, file):
        self.ip = ip
        self.date = datetime.now()
        self.file_id = file.id

    def __repr__(self):
        return "<Log('%r','%r')>" % (self.date, self.ip, self.file.name)


engine = create_engine(DATABASE, echo=SQL_DEBUG)
session = sessionmaker(bind=engine)()


def create_database():
    print "Creating the db...",
    Base.metadata.create_all(engine)
    print "Done."
