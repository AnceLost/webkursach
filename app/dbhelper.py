from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __table_args__ = {"extend_existing": True}

db = SQLAlchemy(model_class=Base)

