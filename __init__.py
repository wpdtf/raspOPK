from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=f"mysql+pymysql://{config.user}:{config.password}@{config.host}/{config.db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.key
db = SQLAlchemy(app)
manager = LoginManager(app)

import routers, models, function
