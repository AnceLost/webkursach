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
from app.crud.base import get_items
from app.models import Game
from app.auth import bp as auth_bp
from app.routes import user_bp
from app.routes import game_bp
from app.factory import create_app


app = create_app()