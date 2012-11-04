#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, flash,
                   url_for, jsonify, abort, make_response)
from flask import request
from flask import redirect

import time
import datetime

from flask import Blueprint
from flask.views import MethodView
from fileexchange.models import File
import os

import struct
import socket


def addressInNetwork(ip, net):
    "Is an address in a network"
    ipaddr = struct.unpack('L', socket.inet_aton(ip))[0]
    netaddr, bits = net.split('/')
    netmask = struct.unpack('L',
                            socket.inet_aton(netaddr))[0] & ((2L<<int(bits)-1) - 1)
    return ipaddr & netmask == netmask

user = Blueprint('user', __name__, template_folder='templates')


class Index(MethodView):

    def get(self):
        try:
            remote = request.headers["X-Forwarded-For"]
            if addressInNetwork(remote, "192.168.0.0/24"):
                return render_template("index.html")
            else:
                abort(403)
        except:
            abort(403)


class FileList(MethodView):
    def get(self):
        files = File.objects(owner=request.headers["X-Forwarded-For"]).order_by("-uploaded")
        return render_template("filelist.html", files=files)


class DeleteFile(MethodView):
    def get(self, id=None):
        try:
            f = File.objects.get(id=id)
            os.unlink(f.path)
            f.delete()
            return "ok"
        except:
            abort(500)


class GetFile(MethodView):
    def get(self, id=None, filename=None):
        try:
            f = File.objects.get(id=id)
            File.objects(id=id).update(inc__count=1)
            File.objects(id=id).update(push__downloadtime=datetime.datetime.now())
            response = make_response()
            response.headers['Cache-Control'] = 'no-cache'
            response.headers['Content-Type'] = f.type
            response.headers['Content-Disposition'] = 'attachment'
            response.headers['X-Accel-Redirect'] = "/download/" + "/".join(f.path.split("/")[3:])
            return response
        except:
            abort(404)


class Uploader(MethodView):

    def post(self):
        res = []
        f = File()
        f.name = request.form["qqfile.name"]
        f.size = request.form["qqfile.size"]
        f.name = request.form["qqfile.name"]
        f.path = request.form["qqfile.path"]
        f.type = request.form["qqfile.content_type"]
        f.md5 = request.form["qqfile.md5"]
        f.savetime = datetime.datetime.now() + datetime.timedelta(hours=int(request.args.get("savetime")))
        f.owner = request.headers["X-Forwarded-For"]
        try:
            f.validate()
            f.save()
        except None:
            return make_response("{\"error\"}")
        return make_response("{\"success\": true}")


user.add_url_rule('/', view_func=Index.as_view('index'))
user.add_url_rule('/filelist', view_func=FileList.as_view('filelist'))
user.add_url_rule('/getfile/<id>/<filename>', view_func=GetFile.as_view('getfile'))
user.add_url_rule('/deletefile/<id>', view_func=DeleteFile.as_view('deletefile'))
user.add_url_rule('/upload', view_func=Uploader.as_view('uploader'))

if __name__ == "__main__":
    pass
