from Languini import db
from flask_login import UserMixin


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns if c.name is not "password"}


@login_manager.user_loader
def load_user(user_name):
    return Admin.query.get(username)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    refNum = db.Column(db.Integer, unique=True)
    vidUrl = db.Column(db.String(120), unique=True, nullable=False)


class Strain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strainType = db.Column(db.String(20))
    LinkCount = db.Column(db.Integer)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strainId = db.Column(db.Integer, db.ForeignKey('Strain.id'), nullable=False)
    nextId = db.Column(db.Integer, nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String)
    moveId = db.Column(db.Integer, db.ForeignKey('Movement.id'), nullable=False)
    linkId = db.Column(db.Integer, db.ForeignKey('Link.id'), nullable=False)


class MoveList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moveId = db.Column(db.Integer, db.ForeignKey('Movement.id'), nullable=False)
    strainId = db.Column(db.Integer, db.ForeignKey('Strain.id'), nullable=False)
