import os
from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature
from werkzeug import secure_filename
from flask.ext.login import current_user, login_user, logout_user
from flask.ext.mail import Message
from app.helpers import login_required, allowed_file
from app import db, login_manager
from .forms import DonationUploadForm, PledgingForm
from .models import Donation

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
    if request.method == 'POST' and form.validate_on_submit():
        file = request.files['upload_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            donation = Donation()
            form.populate_obj(donation)            
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
    return render_template('donors/pledging.html', form=form, error=error)

@donors.errorhandler(413)
def error_handler_413(e):
    return render_template('images/413.html'), 413

@donors.route('/test', methods=['GET', 'POST'])
@login_required
def test_index():
    form = DonationUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        description = form.description.data
        file = form.upload_file.data
        if file and allowed_file(file.filename):
            filename = current_user.username + '_' + secure_filename(file.filename)
            file_content = file.read()
            image_filename = cdn_upload_file(current_user.cdn_folder_name, filename, file_content)
            img_response = requests.get(current_user.cdn_folder_uri + filename)
            img = PIL_Image.open(StringIO(img_response.content))
#            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            donation = Donation()
            donation.title = title
            donation.filename = filename
            donation.user_id = current_user.id
            db.session.add(image)
            db.session.commit()
            return redirect(url_for('.index'))
    donations = db.session.query(Donation).filter(Donation.user_id == current_user.id)
    return render_template('images/index.html', donors=donors, form=form)

@donors.route('/delete/', methods=['POST'])
@donors.route('/delete/<id>', methods=['POST'])
@login_required
def delete_file(id=None):
    """Delete an uploaded file."""
    donor = db.session.query(Donor).get(id)
    if donor and donor.filename:
        try:
            cdn_delete_file(current_user.cdn_folder_name, image.filename)
#            os.remove(image.filename)
        except:
            pass
        db.session.delete(image)
        db.session.commit()
    return redirect(url_for('.index'))

