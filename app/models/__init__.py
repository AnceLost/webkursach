from .user import User
from .userrole import UserRole
from .game import Game, GameGenre, GamePlatform
from .platform import Platform
from .genre import Genre
from .review import Review
from .accesslog import AccessLog

from .base import db
db.configure_mappers()


__all__ = [
    "User",
    "UserRole",
    "Game",
    "Platform",
    "Genre",
    "Review",
    "GamePlatform",
    "GameGenre",
    "AccessLog"
]