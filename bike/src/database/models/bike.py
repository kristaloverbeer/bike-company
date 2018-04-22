from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, JSON

db: SQLAlchemy = SQLAlchemy()


class Bike(db.Model):
    __tablename__ = 'bike'

    id = db.Column(String, primary_key=True)
    status = db.Column(Integer, default=0)
    location = db.Column(JSON)
