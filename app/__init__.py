#! ../env/bin/python
from flask import Flask, render_template, redirect, url_for
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from flask_mail import Mail

Base = declarative_base()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(object_name, env):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    #init SQLAlchemy
    db.init_app(app)
    db.Model = Base

    #Register Mail Service
    mail.init_app(app)

    # Initialize Jinja custom filters
    import filters
    filters.init_app(app)

    # Use Flask-Login to track current user in Flask's sessions
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # register our blueprints
    from app.blueprints import main, auth, orgs, donors
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(orgs)
    app.register_blueprint(donors)
    
    @app.errorhandler(500)
    def error_handler_500(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_handler_404(e):
        return render_template('404.html'), 404

    return app
