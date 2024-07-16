from flask_sqlalchemy import SQLAlchemy

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
    patrols = db.relationship('Patrol', backref='family', lazy=True)

class UsedKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(50), nullable=False)
    patrol_id = db.Column(db.Integer, db.ForeignKey('patrol.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
