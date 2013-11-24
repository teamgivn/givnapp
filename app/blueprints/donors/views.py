import os
from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask import current_app, send_from_directory
from itsdangerous import URLSafeSerializer, BadSignature
from werkzeug import secure_filename
from flask.ext.login import current_user, login_user, logout_user
from flask.ext.mail import Message
from app.helpers import login_required, allowed_file
from app import db, login_manager
from .models import Donation
from .forms import DonationUploadForm, PledgingForm
from .models import Donation

donors = Blueprint(
    'donors', 
    __name__,
    template_folder='templates', 
    url_prefix='/donors'
)

@donors.route('/uploads/<filename>/')
def uploads(filename):
    return url_for('static', filename='uploads/' + filename)
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@donors.route('/', methods=['GET', 'POST'])
def index():
    error = None
    donations = db.session.query(Donation).filter(Donation.user_id==current_user.id).all()
    return render_template('donors/index.html', error=error, donations=donations)

@donors.route('/create/', methods=['GET', 'POST'])
def create():
    error = None
    form=DonationUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['upload_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            donation = Donation()
            form.populate_obj(donation)
            donation.type = 2            
            donation.filename = filename
            donation.user_id = current_user.id
            db.session.add(donation)
            db.session.commit()
            return redirect(url_for('donors.index'))
    return render_template('donors/create.html', form=form, error=error)

@donors.route('/pledging/', methods=['GET', 'POST'])
def pledging():
    error = None
    form=PledgingForm()
    if request.method == 'POST' and form.validate_on_submit():
        donation = Donation()
        form.populate_obj(donation)       
        donation.type = 1     
        donation.user_id = current_user.id
        db.session.add(donation)
        db.session.commit()
        return redirect(url_for('donors.index'))
    return render_template('donors/pledging.html', form=form, error=error)

@donors.errorhandler(413)
def error_handler_413(e):
    return render_template('images/413.html'), 413

@donors.route('/delete/', methods=['POST'])
@donors.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id=None):
    """Delete an uploaded file."""
    donation = db.session.query(Donation).get(id)
    if donor and donation.filename:
        try:
            filename = secure_filename(file.filename)
            file.delete(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        except:
            pass
        db.session.delete(donation)
        db.session.commit()
    return redirect(url_for('.index'))
