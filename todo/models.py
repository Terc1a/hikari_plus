from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    tag = db.Column(db.String(50))
    descr = db.Column(db.String(1000))
    is_complete = db.Column(db.Boolean)