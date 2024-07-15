from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    time_penalty = db.Column(db.Integer, default=0)

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    patrols = db.relationship('Patrol', backref='family', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    keyword = db.Column(db.String(50), nullable=False)
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'), nullable=False)
    sequence = db.Column(db.Integer, nullable=False)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    families = db.relationship('Family', backref='route', lazy=True)

