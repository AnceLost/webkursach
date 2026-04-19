from .base import *

class Genre(Base):
    __tablename__ = 'genres'
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(200))