#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server, Command
from fileexchange import app

app.debug = True
manager = Manager(app)


# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0',
    port = 6789)
)

class GeventServer(Command):
    def run(self):
        
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('', 6789), app)
        http_server.serve_forever()

class CreateDb(Command):
    def run(self):
        from fileexchange import db
        db.create_all()

manager.add_command("gevent_server", GeventServer())
manager.add_command("create_db", CreateDb())

if __name__ == "__main__":
    manager.run()
