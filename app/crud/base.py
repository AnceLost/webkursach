from sqlalchemy.exc import SQLAlchemyError

from app.dbhelper import db
from app.models import User, Game, Genre, Platform
from app.exceptions import (DatabaseUpdateError, 
                            DatabaseNotFoundError, 
                            DatabaseCreateEntityError, 
                            DatabaseDeleteEntityError,
                            DatabaseError)