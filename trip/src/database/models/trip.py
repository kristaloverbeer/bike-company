import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, JSON

db: SQLAlchemy = SQLAlchemy()


class Trip(db.Model):
    __tablename__ = 'trip'

    id = db.Column(String, primary_key=True)
    status = db.Column(Integer, default=0)
    bike_id = db.Column(String)
    locations = db.Column(JSON)
    started_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = db.Column(DateTime, default=None)
