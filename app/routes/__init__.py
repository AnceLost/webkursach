from .user import bp as user_bp
from .game import bp as game_bp
from .admin import bp as admin_bp

__all__ = [
    "user_bp",
    "game_bp",
    "admin_bp"
]