from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature
from flask.ext.login import current_user, login_user, logout_user
from flask.ext.mail import Message
from app.helpers import login_required
from app import db, login_manager
from .forms import DonationUploadForm

donors = Blueprint(
    'donors', 
    __name__,
    template_folder='templates', 
    url_prefix='/donors'
)

@donors.route('/', methods=['GET', 'POST'])
def index():
    error = None
    return render_template('donors/index.html', error=error)

@donors.route('/create/', methods=['GET', 'POST'])
def create():
    error = None
    form=DonationUploadForm()
    return render_template('donors/create.html', form=form, error=error)