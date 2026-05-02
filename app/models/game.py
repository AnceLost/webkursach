from .base import *
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

class Game(Base):
    __tablename__ = 'games'
    
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    release_date: Mapped[datetime] = mapped_column(nullable=True)
    cover_path: Mapped[str] = mapped_column(String(256), nullable=True, server_default="defaultcover.jpg")
    
    #строим связи
    reviews: Mapped[List["Review"]] = relationship(back_populates="game")
    platforms: Mapped[List["Platform"]] = relationship(back_populates="games",secondary="games_platforms")
    genres: Mapped[List["Genre"]] = relationship(back_populates="games", secondary="games_genres")
    
    @property
    def cover_uri(self):
        return url_for('static', filename=f'upload/covers/{self.cover_path}')
    
    @property
    def average_rating(self) -> float:
        res = 0
        for rev in self.reviews:
            res += rev.mark
        res = res/self.review_count if self.review_count > 0 else 0
        return round(res, 1) if res else 0
    
    @property
    def review_count(self) -> int:
        return len(self.reviews)
    
class GamePlatform(Base):
    __tablename__ = 'games_platforms'
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
    platform_id: Mapped[int] = mapped_column(ForeignKey("platforms.id", ondelete="CASCADE"), primary_key=True)
    
    
class GameGenre(Base):
    __tablename__ = 'games_genres'
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True)
  