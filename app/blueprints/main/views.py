from flask import Blueprint, render_template, session, redirect, url_for, request, abort
from flask import current_app

main = Blueprint(
    'main', 
    __name__,
    template_folder='templates'
)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@main.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')

@main.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico'))

@main.errorhandler(413)
def error_handler_413(e):
    return 'file size too large', 413