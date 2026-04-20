import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
#для миграций - export FLASK_APP='main.py'
from datetime import datetime

from flask import (
    Flask, request, session, 
    url_for, redirect, render_template, 
    flash, make_response, Blueprint)
from auth import init_login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Settings
from app.dbhelper import db
from app.auth import bp as auth_bp


app = Flask(__name__)

settings = Settings()

app.secret_key = settings.get_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = settings.get_db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
init_login_manager(app)

app.register_blueprint(auth_bp)

@app.context_processor
def inject_getattr():
    return dict(getattr=getattr)

@app.route('/')
def index():
    return render_template('index.html')