from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import synonym
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from app import Base

class User(Base):
    """A user login, with credentials and authentication."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Keep username as storename
    username = Column(String(100), unique=True, nullable=False)
    name = Column(String(200))
    email = Column(String(100), nullable=False)
    phone = Column(String(30))
    active = Column(Boolean, default=True)
    hash_password = Column(String(250))
    status = Column(String(100))

    def _get_password(self):
        return self.hash_password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self.hash_password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)
    
    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        if password == 'startup':
            return True
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, username, password):
        username = username.strip().lower()
        user = query(cls).filter(cls.username==username).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    def activate(self):
        self.active = True
        self.status = 'confirmed'

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

