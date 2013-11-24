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
    frequency = Column(String(60))
    recurring_number = Column (String(2))
    description = Column(String(60))
    filename = Column(String(100))
    amount = Column(String(30))
    payment_type = Column(String(30))
    receipt = Column(Boolean)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    user = relationship("User", backref="donations")
    type = Column(Integer)

    def __init__(self):
        pass

