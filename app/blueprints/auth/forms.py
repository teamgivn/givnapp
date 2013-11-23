from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, PasswordField, BooleanField, validators
from wtforms.validators import Required, EqualTo, Email

class LoginForm(Form):
    username = TextField('User Name:', [Required()])
    password = PasswordField('Password:', [Required()])
    rememberme = BooleanField('Remember me')


class RegisterForm(Form):
    username = TextField('User Name:', [Required()])
    password = PasswordField('Password:', [Required()])
    confirm = PasswordField('Repeat Password:', [
        Required(),
        EqualTo('password', message='Passwords must match')
        ])
    name = TextField('Contact Name (for support only):')
    phone = TextField('Phone Number (for support only):')
    email = TextField('Email address (for verification only):', [Required(), Email()])
    accept_tos = BooleanField('I agree to <a href="http://givn.us">Givn Terms</a>', [Required()])


class AccountSettingsForm(Form):
    username = TextField('User Name:')
    password = PasswordField('Password:')
    confirm = PasswordField('Repeat Password:', [
        EqualTo('password', message='Passwords must match')
        ])
    name = TextField('Contact Name:', [Required()])
    phone = TextField('Phone Number (optional):')
    email = TextField('Email address:', [Required(), Email()])