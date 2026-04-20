from .user import User
from .userrole import UserRole
from .game import *
from .platform import Platform
from .genre import Genre
from .review import Review

from .base import db
db.configure_mappers()


__all__ = [
    "User",
    "UserRole",
    "Game",
    "Platform",
    "Genre",
    "GamePlatform",
    "GameGenre"
]