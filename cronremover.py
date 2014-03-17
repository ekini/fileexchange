#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

from fileexchange import db
from fileexchange.models import File

def main():
    for file in db.session.query(File).filter(File.deletion_date <= datetime.now()):
        print "Deleting '%s' (owner: %s): %s" % (file.name,
                                                 file.owner,
                                                 file.path)
        os.unlink(doc["path"])
        db.file.remove({"_id": doc["_id"]})

if __name__ == "__main__":
        main()
