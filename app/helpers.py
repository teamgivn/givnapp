from os import urandom, path
from datetime import datetime
from functools import wraps
import json
from flask import session, g, redirect, current_app, jsonify
from flask.ext.login import login_required as flask_ext_login_required
from flask.ext.login import current_user as flask_ext_current_user
from flask.ext.mail import Message
from app import mail, db


login_required = flask_ext_login_required
current_user = flask_ext_current_user

def send_email(recipients, subject, body):
    """
    Send the awaiting for confirmation mail to the user.
    """
    msg = Message(subject=subject, sender=current_app.config['MAIL_SENDER'], recipients=recipients)
    msg.body =  body
#    msg.html = '<b>HTML</b> body'
    with current_app.app_context():
        mail.send(msg)
        return True