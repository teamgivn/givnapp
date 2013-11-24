from datetime import datetime
from sqlalchemy import Column, Boolean, Integer, String, DateTime, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import synonym, relationship
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from app import Base


class Donation(Base):
    __tablename__ = 'donations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    organization = Column(String(60))
    description = Column(String(60))
    filename = Column(String(100))
    amount = Column(String(30))
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship("User", backref="donations")
    organization = relationship("organization", backref="donations")

    def __init__(self):
        pass

