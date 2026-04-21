from .base import *

class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[intpk]
    mark: Mapped[int] = mapped_column(CheckConstraint("mark => 1 AND mark <= 5"))
    text: Mapped[str]
    
    #связи с игрой и пользователем 
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="reviews")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship()
    created_at: Mapped[createdAt]
    updated_at: Mapped[updatedAt]