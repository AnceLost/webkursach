from datetime import datetime
import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, MetaData
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Optional, Union, List, Annotated

from dbhelper import db, Base

intpk = Annotated[int, mapped_column(primary_key=True, init=False)]
created_at = Annotated[datetime, mapped_column(server_default=db.func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=db.func.now(), onupdate=db.func.now())]

class UserRole(Base):
    __tablename__ = 'userroles'
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int] = mapped_column(default=0) #Что-то типа уровня допуска
    
class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(String(50))
    nickname: Mapped[str] = mapped_column(String(50)) #Это имя будет видно другим пользователям
    role_id: Mapped[int] = mapped_column(ForeignKey("userroles.id"))
    role: Mapped[UserRole] = relationship()
    
    
    