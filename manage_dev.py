#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from app import create_app

env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('app.settings.%sConfig' % env.capitalize(), env)
app.debug = True

manager = Manager(app)

manager.add_command("runserver", \
                    Server(use_debugger = True, use_reloader = True))

@manager.shell
def make_shell_context():
    """Creates a python REPL with several default imports in the context of the app"""
    return dict(app=app)


if __name__ == "__main__":
    manager.run()