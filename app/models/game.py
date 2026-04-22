from .base import *

class Game(Base):
    __tablename__ = 'games'
    
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str]
    release_date: Mapped[datetime]
    cover_path: Mapped[str] = mapped_column(String(256), nullable=True, server_default="defaultcover.jpg")
    
    #строим связи
    reviews: Mapped[List["Review"]] = relationship(back_populates="game")
    platforms: Mapped[List["GamePlatform"]] = relationship(back_populates="game")
    genres: Mapped[List["GameGenre"]] = relationship(back_populates="game")
    
    @property
    def cover_uri(self):
        return url_for('static', filename=f'upload/covers/{self.cover_path}')
    
class GamePlatform(Base):
    __tablename__ = 'games_platforms'
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id", ondelete="CASCADE"), primary_key=True)
    
    game: Mapped["Game"] = relationship(back_populates="platforms")
    
    """
    такую штуку не надо, так как платформам не обязательно знать какие игры на них запускаются    
    platform: Mapped["Platform"] = relationship(back_populates="games")
    """
    
class GameGenre(Base):
    __tablename__ = 'games_genres'
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
    
    game: Mapped["Game"] = relationship(back_populates="genres")
    
    """
    такую штуку не надо, так как жанрам не обязательно знать какие игры в них включены
    genre: Mapped["Genre"] = relationship(back_populates="games")
    """