import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from app.dbhelper import db
from app.crud.base import get_items
from app.models import Game
from app.auth import init_login_manager
from app.config import Settings


csrf = CSRFProtect()

def create_app(settings=None):
    if settings is None:
        settings = Settings()   # загружает переменные из .env
        
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024   # 5 MB

    for field_name in settings.model_fields:
        value = getattr(settings, field_name)
        # Не перезаписываем уже установленные ключи (SECRET_KEY и т.п.)
        if field_name not in app.config:
            app.config[field_name] = value

    db.init_app(app)
    migrate = Migrate(app, db)
    init_login_manager(app)
    csrf.init_app(app)

    # Регистрация blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    from app.routes import game_bp, user_bp, admin_bp, genre_bp, platform_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(genre_bp)
    app.register_blueprint(platform_bp)
    
    @app.context_processor
    def inject_getattr():
        return dict(getattr=getattr)

    @app.route('/')
    def index():
        latest_games = get_items(Game, per_page=5)
        return render_template('index.html', latest_games=latest_games)

    return app