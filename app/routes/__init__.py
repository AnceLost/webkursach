from .user import bp as user_bp
from .game import bp as game_bp
from .admin import bp as admin_bp
from .genre import bp as genre_bp
from .platform import bp as platform_bp

__all__ = [
    "user_bp",
    "game_bp",
    "admin_bp",
    "genre_bp",
    "platform_bp"
]