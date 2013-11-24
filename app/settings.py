import os

class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    # email server
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'teamgivn@gmail.com'
    MAIL_PASSWORD = '43046721'
    # Mail Sender list
    MAIL_SENDER = 'teamgivn@gmail.com'
    #Upload of files
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPEG', 'GIF', 'PNG', 'JPG'])
    UPLOAD_FOLDER = BASE_DIR + '/static/uploads'

class ProdConfig(Config):
    SECRET_KEY = 'givn - The next big startup'
    # Shoppify settings
    CACHE_TYPE = 'simple'
    # SQL Alchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_prod.sqlite'

class DevConfig(Config):
    SECRET_KEY = 'givn dev - startupweekend'
    DEBUG = True
    CACHE_TYPE = 'null'
    # SQL Alchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_dev.sqlite'
    SQLALCHEMY_ECHO = True

class DevManageConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app/app_dev.sqlite'

class ProdManageConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app/app_prod.sqlite'

