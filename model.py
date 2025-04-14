from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class HeartResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    prediction = db.Column(db.String(20))
  

class DiabetesResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    prediction = db.Column(db.String(20))

class ParkinsonResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    prediction = db.Column(db.String(20))
     
