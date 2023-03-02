from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    super_user = db.Column(db.Boolean, default=False)
    money = db.Column(db.Integer, default=0)
    tasks = db.relationship('Tasks', backref='user')

    def is_admin(self):
        return self.super_user


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson = db.Column(db.Integer)
    task = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    is_check = db.Column(db.Boolean)
    text = db.Column(db.String())
