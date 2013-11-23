from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature
from flask.ext.login import current_user, login_user, logout_user
from flask.ext.mail import Message
from app.helpers import login_required
from app import db, login_manager

orgs = Blueprint(
    'orgs', 
    __name__,
    template_folder='templates', 
    url_prefix='/orgs'
)

@orgs.route('/', methods=['GET', 'POST'])
def index():
    error = None
    return render_template('orgs/index.html', error=error)
