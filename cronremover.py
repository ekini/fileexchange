#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import Connection
import os
import datetime

db = Connection().upload

def main():
    for doc in db.file.find({"savetime": {"$lt": datetime.datetime.now()}}):
        print "Deleting %s (owner: %s): %s" % (doc["name"], doc["owner"], doc["path"])
        os.unlink(doc["path"])
        db.file.remove({"_id": doc["_id"]})

if __name__ == "__main__":
        main()

