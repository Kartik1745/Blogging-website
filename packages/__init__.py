from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']='e0e1d02d982b26e44a4c6101e8a624bc'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
Login_manager=LoginManager(app)
Login_manager.login_view='login'
Login_manager.login_message_category='info'

from packages import routes