from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

db = SQLAlchemy()
migrate = Migrate(db)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    tag_id = db.Column(db.Integer)
    descr = db.Column(db.String(1000))
    create_date = db.Column(db.DateTime)
    close_date = db.Column(db.DateTime)
    is_complete = db.Column(db.Boolean)
    is_cycle = db.Column(db.String(25))
    cycle_series = db.Column(db.Integer)
    time_to_complete = db.Column(db.String(100))
    responsible = db.Column(db.Integer)
    # chlist = db.Column(db.PickleType) неактуально после добавления модели Checks, не удаляю окончательно, так как не до конца понятны недостатки нового подхода


class Checks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer)
    text = db.Column(db.String(1000))
    is_checked = db.Column(db.Boolean)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    ws_id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(1000))


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(1000))


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    descr = db.Column(db.String(1000))
    version = db.Column(db.String(10))
    create_date = db.Column(db.String(25))
    to_send = db.Column(db.Boolean)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    register_date = db.Column(db.String(100))
    avatar = db.Column(db.LargeBinary)