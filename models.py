from exts import db
from datetime import datetime


class Todo(db.Model):
    __tablename__ = 'Todo list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(101), unique=True)
    content = db.Column(db.String(255))
    creat_time = db.Column(db.DateTime, default=datetime.now, index=True)
    status = db.Column(db.Boolean)

    def __init__(self, title, content, status):
        self.title = title
        self.content = content
        self.status = status

    def get_title(self):
        return self.title

    def __repr__(self):
        return "<Todo %r>" % self.title


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = self.set_password(password)

