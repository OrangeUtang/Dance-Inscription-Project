from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '5315ad021c9bdbeb55396e378f9ada298274c9a2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab.db'
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from langlab import routes
