from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin

Base = declarative_base()


class User(UserMixin, db.Model, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    food = relationship('Food', back_populates='parent_user')


class Food(db.Model, Base):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    parent_user = relationship('User', back_populates='food')
    parent_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


db.create_all()
