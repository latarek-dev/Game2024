from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType

db = SQLAlchemy()

class Patrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    time_penalty = db.Column(db.Integer, default=0)
    password = db.Column(db.String(128), nullable=False, default='default_password')  # Dodajemy domyślne hasło
    used_keywords = db.relationship('UsedKeyword', backref='patrol', lazy=True)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    discovered_magazines = db.Column(db.Integer, default=0)
    patrols = db.relationship('Patrol', backref='family', lazy=True)
    assigned_magazines = db.Column(MutableList.as_mutable(PickleType), default=[])
    tasks = db.relationship('FamilyTask', backref='family', lazy=True)
    magazine_list = db.Column(db.String(1), nullable=False, default='a')  # 'a', 'b', 'c', 'd', 'e', or 'f'
    end_time = db.Column(db.DateTime, nullable=True)
    route = db.Column(db.String(1), nullable=False)  # Dodane pole dla drogi ('a' albo 'b')
    meeting_place = db.Column(db.String(255), nullable=True)  # Nowe pole dla miejsca spotkania

class UsedKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    patrol_id = db.Column(db.Integer, db.ForeignKey('patrol.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class FamilyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)