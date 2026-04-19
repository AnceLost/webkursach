from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Text, Integer, MetaData, CheckConstraint
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from typing import Optional, Union, List, Annotated

from app.dbhelper import db, Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=db.func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=db.func.now(), onupdate=db.func.now())]




# Ещё вот так можно одинаковые типы миксовать и подключать

# class TimestampMixin:
#     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())

# class PrimaryKeyMixin:
#     id: Mapped[int] = mapped_column(primary_key=True)

# class User(PrimaryKeyMixin, TimestampMixin, Base):