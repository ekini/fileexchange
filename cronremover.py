#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime

from models import session, File

def main():
    for file in session.query(File).filter(File.deletion_date <= datetime.now()):
        print "Deleting '%s' (owner: %s): %s" % (file.name,
                                                 file.owner,
                                                 file.path)
        os.unlink(doc["path"])
        db.file.remove({"_id": doc["_id"]})

if __name__ == "__main__":
        main()
