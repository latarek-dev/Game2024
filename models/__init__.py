from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    patrols = db.relationship('Patrol', backref='family', lazy=True)

class Patrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    time_penalty = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='patrol', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    keyword = db.Column(db.String(50), nullable=False)
    patrol_id = db.Column(db.Integer, db.ForeignKey('patrol.id'), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)
