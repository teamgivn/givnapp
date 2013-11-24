from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, PasswordField, BooleanField, FileField, validators
from wtforms.validators import Required, EqualTo, Email


class DonationUploadForm(Form):
    organization = SelectField('Organization:', choices=[('Other', "Other"), ('United Health', "United Health"), ('Austin Goodwill', "Austin Goodwill"), ('ASGA Austin', "ASGA Austin")], default='1')
    frequency = SelectField('Frequency:', choices=[('1', "One-off"), ('2', "Recurring")], default='1')
    recurring_number = TextField('Number Per Year')
    amount = TextField('Amount', [validators.Required()])
    payment_type = SelectField('Payment Type', choices=[('1', "Credit Card"), ('2', "Bank Transfer"), ('3', "Cash")], default='1')
    description = TextField('Description:', [validators.Required()])
    upload_file = FileField('Choose image file (max 1MB):')
    receipt = BooleanField('Receipt:')

class PledgingForm(Form):
    organization = SelectField('Organization:', choices=[('1', "Other"), ('2', "United Health"), ('3', "Austin Goodwill"), ('4', "ASGA Austin")], default='1')
    frequency = SelectField('Frequency:', choices=[('1', "One-off"), ('2', "Recurring")], default='1')
    recurring_number = TextField('Number Per Year')
    amount = TextField('Amount', [validators.Required()])
    description = TextField('Description:', [validators.Required()])