from flask import Blueprint, render_template, session, redirect, url_for, request, abort, flash
from flask import current_app
from itsdangerous import URLSafeSerializer, BadSignature
from flask.ext.login import current_user, login_user, logout_user
from flask.ext.mail import Message
from app.helpers import login_required
from app import db, login_manager, mail
from .models import User
from .forms import LoginForm, RegisterForm, AccountSettingsForm


auth = Blueprint(
    'auth', 
    __name__,
    template_folder='templates', 
    url_prefix='/users'
)


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login hook to load a User instance from ID"""
    return db.session.query(User).get(user_id)

def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = current_app.config['SECRET_KEY']
    return URLSafeSerializer(secret_key)

def get_activation_link(user):
    s = get_serializer()
    payload = s.dumps(user.id)
    return url_for('auth.activate_user', payload=payload, _external=True)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
            return redirect(url_for('orgs.index'))
    form = LoginForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower().strip()
        password = form.password.data
        user, authenticated = User.authenticate(db.session.query, username, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('orgs.index'))
        else:
            error = 'Incorrect username or password'
    return render_template('auth/login.html', form=form, error=error)

@auth.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/settings/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    user = db.session.query(User).get(user_id)
    error = None
    if request.method == 'GET':
        form = AccountSettingsForm(obj=user)
    elif request.method == 'POST':
        form = AccountSettingsForm()
        if form.validate_on_submit():
        # insert into db
            user.name = form.name.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.shop_realtime = form.shop_realtime.data
            if form.password.data:
                user.password = form.password.data
            db.session.commit()
            return redirect(url_for('auth.settings', user_id=user.id))
    # On Error render index page
    user = db.session.query(User).get(user_id)
    return render_template('auth/settings.html', user=user, form=form, error=error )

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        new_user = User()
        new_user.username = form.username.data
        new_user.name = form.name.data
        new_user.password = form.password.data
        new_user.email = form.email.data
        new_user.phone = form.phone.data
        new_user.active = False
        new_user.status = 'awaiting_confirm'
        db.session.add(new_user)
        db.session.commit()
        ### Registering the new user here* ###
        activation_url = get_activation_link(new_user)
        send_awaiting_confirm_mail(new_user, message_url=activation_url)
        flash("Email Verification sent. Please confirm your account activation via e-mail", 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, error=error )


@auth.route('/activate/<payload>/')
def activate_user(payload):
    s = get_serializer()
    try:
        user_id = s.loads(payload)
    except BadSignature:
        abort(404)
    user = db.session.query(User).get(user_id)
    if not user:
        return abort(404)
    user.activate()
    db.session.commit()
    flash('Your Account is now Active.  Please reach us teamgivn@gmail.com if you have any questions')
    flash('We offer free setup and help you take control of your store displays.')
    return redirect(url_for('auth.login'))


def send_awaiting_confirm_mail(user, message_url):
    """
    Send the awaiting for confirmation mail to the user.
    """
    subject = "Welcome to Givn"
    msg = Message(subject=subject, sender=current_app.config['MAIL_SENDER'], recipients=[user.email])
    msg.body =  """
    Dear %s,
    Thank you for signing up for Givn to give you greater control over your website display and measure what works.  There's one last thing before you can upload images and start running your carousel sliders.  Please confirm your account by clicking on this link: %s
        
    Thanks,
    Givn Team
    teamgivn@gmail.com
    """ %(user.name, message_url)
#    msg.html = '<b>HTML</b> body'
    with current_app.app_context():
        mail.send(msg)
