#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import time

from flask import (Flask, render_template, flash,
                   url_for, jsonify, abort, make_response)
from flask import request
from flask import redirect

from netaddr import IPAddress, IPNetwork
from shortuuid import uuid


from flask import Blueprint
from flask.views import MethodView
from fileexchange.models import session, File, Log

user = Blueprint('user', __name__, template_folder='templates')


class Index(MethodView):

    def get(self):
        try:
            remote = request.headers["X-Forwarded-For"]
            if IPAddress(remote) in IPNetwork("192.168.0.0/24"):
                return render_template("index.html")
            else:
                abort(403)
        except None:
            abort(403)


class FileList(MethodView):
    def get(self):
        files = session.query(File).filter_by(owner=request.headers["X-Forwarded-For"]).order_by("-upload_date")
        return render_template("filelist.html", files=files)


class DeleteFile(MethodView):
    def get(self, id=None):
        try:
            f = session.query(File).filter_by(owner=request.headers["X-Forwarded-For"], uuid=id).first()
            if f:
                os.unlink(f.path)
                f.delete()
                return "ok"
        except:
            abort(500)


class GetFile(MethodView):
    def get(self, id=None, filename=None):
        try:
            f = session.query(File).filter_by(uuid=id).first()
            if f:
                log = Log(request.headers["X-Forwarded-For"], f)
                session.add(log)
                session.commit()
                response = make_response()
                response.headers['Cache-Control'] = 'no-cache'
                response.headers['Content-Type'] = f.type
                response.headers['Content-Disposition'] = 'attachment'
                response.headers['X-Accel-Redirect'] = "/download/" + "/".join(f.path.split("/")[3:])
                return response
        except:
            session.rollback()
            abort(404)


class Uploader(MethodView):
    def post(self):
        res = []
        f = File()
        f.uuid = uuid()
        f.name = request.form["qqfile.name"]
        f.size = request.form["qqfile.size"]
        f.path = request.form["qqfile.path"]
        f.owner = request.headers["X-Forwarded-For"]
        f.type = request.form["qqfile.content_type"]
        f.md5 = request.form["qqfile.md5"]
        f.deletion_date = datetime.datetime.now() + datetime.timedelta(hours=int(request.args.get("savetime")))
        f.upload_date = datetime.datetime.now()
        try:
            session.add(f)
            session.commit()
        except:
            session.rollback()
            return make_response("{\"error\"}")
        return make_response("{\"success\": true}")


user.add_url_rule('/', view_func=Index.as_view('index'))
user.add_url_rule('/filelist', view_func=FileList.as_view('filelist'))
user.add_url_rule('/getfile/<id>/<filename>', view_func=GetFile.as_view('getfile'))
user.add_url_rule('/deletefile/<id>', view_func=DeleteFile.as_view('deletefile'))
user.add_url_rule('/upload', view_func=Uploader.as_view('uploader'))

if __name__ == "__main__":
    pass
