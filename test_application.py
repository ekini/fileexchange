#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import datetime

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fileexchange
from fileexchange.models import File


class FileexchangeTestCase(unittest.TestCase):

    testfile = File(name="test_file.py", type="application/python",
             owner="192.168.0.1", path="/dev/null",
             md5="123", savetime=datetime.datetime.now(),
             size="12345")

    def setUp(self):
        self.app = fileexchange.app.test_client()
        self.db = fileexchange.db

    def tearDown(self):
        pass

    def test_filemodel(self):
        """Validates file object"""
        f = self.testfile
        f.validate()

    def test_access(self):
        response = self.app.get("/",
                                headers={"X-Forwarded-For": "10.1.0.4"})
        self.assertEqual(response.status_code, 403, "The code must be 403")

    def test_index(self):
        """Tests the status code for the right network"""
        response = self.app.get("/",
                                headers={"X-Forwarded-For": "192.168.0.4"})
        self.assertEqual(response.status_code, 200, "Must be 200")

    def test_filelist(self):
        """Tests the presence of file in list"""
        self.testfile.save(safe=True)

        response = self.app.get("/filelist",
                                headers={"X-Forwarded-For": "192.168.0.1"})
        self.assertTrue(self.testfile.name in response.data,
                        "Filename must be in the list")

        self.testfile.delete(safe=True)


if __name__ == '__main__':
    unittest.main()
