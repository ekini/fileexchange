#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import Connection
import os
import datetime

db = Connection().upload

def main():
    for doc in db.file.find({"savetime": {"$lt": datetime.datetime.now()}}):
        print "Deleting %s: %s" % (doc["name"], doc["path"])
        os.unlink(doc["path"])
        doc.delete()

if __name__ == "__main__":
        main()

