import os
DEBUG = True
DIALECT = 'mysql'
USERNAME = 'root'
PASSWORD = '666'
HOST = 'localhost'
DATABASE = 'todolist'

#SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}?charset=utf8".format(DIALECT, USERNAME, PASSWORD, HOST, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False