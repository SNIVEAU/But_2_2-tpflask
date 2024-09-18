from flask import Flask
from flask_bootstrap import Bootstrap5
app = Flask(__name__)
import os.path
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
def mkpath(p):
    return os.path.normpath(os.path.join(
os.path.dirname(__file__),
p))
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (
'sqlite:///'+mkpath('../myapp.db'))
db = SQLAlchemy(app)
app. config['SECRET_KEY']="9d088f4d-de8b-449b-9c8a-4f3551a578cd"
