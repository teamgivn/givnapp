#!/bin/bash

# source - http://community.webfaction.com/questions/12718/installing-flask
# First, fill in these variables with your Application Name and URL Path:

APPNAME="givnapp"
URLPATH="/givnapp"

rm -r $HOME/webapps/$APPNAME/htdocs
mkdir $HOME/webapps/$APPNAME/$APPNAME

# Step 2
# deploy the app
# cd $HOME
# mkdir -p $HOME/webapps/$APPNAME/lib/python2.7
# cd $HOME/webapps/$APPNAME/$APPNAME/
# virtualenv env

#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 Flask
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 Flask-SqlAlchemy
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 Flask-Script
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 Flask-Migrate
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 config
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 six
#pip-2.7 install --install-option=--install-lib=$HOME/webapps/$APPNAME/lib/python2.7 Flask-Restful

# easy_install-2.7 flask

touch $HOME/webapps/$APPNAME/$APPNAME/__init__.py
touch $HOME/webapps/$APPNAME/$APPNAME/index.py
echo "import sys" > $HOME/webapps/$APPNAME/wsgi.py
echo "sys.path.insert(0, '$HOME/webapps/$APPNAME')" >> $HOME/webapps/$APPNAME/wsgi.py
echo -e "from $APPNAME import app as application\n" >> $HOME/webapps/$APPNAME/wsgi.py
sed -i "s^WSGILazyInitialization On^WSGILazyInitialization On\nWSGIScriptAlias / $HOME/webapps/$APPNAME/wsgi.py^" $HOME/webapps/$APPNAME/apache2/conf/httpd.conf
sed -i "s^AddHandler wsgi-script .py^AddHandler wsgi-script .py\n    RewriteEngine on\n    RewriteBase /\n    WSGIScriptReloading On^" $HOME/webapps/$APPNAME/apache2/conf/httpd.conf
sed -i "s/htdocs/$APPNAME/g" $HOME/webapps/$APPNAME/apache2/conf/httpd.conf

cat << EOF >> $HOME/webapps/$APPNAME/$APPNAME/__init__.py
from flask import Flask
app = Flask(__name__)

EOF

if [[ "$URLPATH" != "/" ]]; then
cat << EOF >> $HOME/webapps/$APPNAME/$APPNAME/__init__.py
class WebFactionMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = '$URLPATH'
        return self.app(environ, start_response)

app.wsgi_app = WebFactionMiddleware(app.wsgi_app)

EOF
fi

cat << EOF >> $HOME/webapps/$APPNAME/$APPNAME/__init__.py
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
EOF

# Step 3
$HOME/webapps/$APPNAME/apache2/bin/restart