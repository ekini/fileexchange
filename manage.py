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
    host = '0.0.0.0')
)

class GeventServer(Command):
    def run(self):
        
        from gevent.wsgi import WSGIServer

        http_server = WSGIServer(('', 5000), app)
        http_server.serve_forever()

manager.add_command("gev", GeventServer())

if __name__ == "__main__":
    manager.run()
