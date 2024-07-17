from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType

db = SQLAlchemy()

class Patrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    time_penalty = db.Column(db.Integer, default=0)
    used_keywords = db.relationship('UsedKeyword', backref='patrol', lazy=True)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    discovered_magazines = db.Column(db.Integer, default=0)
    patrols = db.relationship('Patrol', backref='family', lazy=True)
    assigned_magazines = db.Column(MutableList.as_mutable(PickleType), default=[])
    tasks = db.relationship('FamilyTask', backref='family', lazy=True)
    magazine_list = db.Column(db.String(1), nullable=False, default='a')  # 'a', 'b', 'c', 'd', 'e', or 'f'

class UsedKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    patrol_id = db.Column(db.Integer, db.ForeignKey('patrol.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class FamilyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)