import sys
import os

sys.path.insert(0, '/home/givn/webapps/givnapp/givnapp')
activate_this = "/home/givn/webapps/givnapp/givnapp/env/bin/activate_this.py"
execfile(activate_this, {"__file__": activate_this})

from app import create_app

env = os.environ.get('APPNAME_ENV', 'prod')
app = create_app('app.settings.%sConfig' % env.capitalize(), env)

class WebFactionMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = '/givnapp'
        return self.app(environ, start_response)

app.wsgi_app = WebFactionMiddleware(app.wsgi_app)

application = app
