from .base import *

class Genre(Base):
    __tablename__ = 'genres'
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(200))
    
    games: Mapped[List["Game"]] = relationship(back_populates="genres", secondary="games_genres")