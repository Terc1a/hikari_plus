from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    tag = db.Column(db.String(50))
    descr = db.Column(db.String(1000))
    create_date = db.Column(db.String(25))
    close_date = db.Column(db.String(25))
    is_complete = db.Column(db.Boolean)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(1000))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(1000))
    version = db.Column(db.String(10))
    create_date = db.Column(db.String(25))
    to_send = db.Column(db.Boolean)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    register_date = db.Column(db.String(100))