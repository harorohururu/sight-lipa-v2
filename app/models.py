from . import db
from datetime import datetime

class Landmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(256), nullable=False)
    qr_code_path = db.Column(db.String(256))
    visits = db.relationship('VisitLog', backref='landmark', lazy=True)

class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    landmark_id = db.Column(db.Integer, db.ForeignKey('landmark.id'), nullable=False)
    tourist_info = db.Column(db.String(256))  # Optional: can be extended
