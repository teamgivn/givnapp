#!/usr/bin/env python
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db

env = os.environ.get('APPNAME_ENV', 'prod')
app = create_app('app.settings.%sManageConfig' % env.capitalize(), env)
app.debug = True

manager = Manager(app)

# Setup SQLAlchemy migration
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()