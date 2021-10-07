from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e881321ec34810873cb4d5b3e1946141'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

from flaskblog import routes 