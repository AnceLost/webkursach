from datetime import datetime

from .base import *
from app.utils import delete_image

def search_games(title_contains: str = None, 
                 genre_ids: List[int] = None, 
                 page: int = 1, 
                 per_page: int = 20) -> List[Game]:
    """Поиск игр по названию, жанрам"""
    query = db.select(Game)
    if title_contains:
        query = query.where(Game.title.contains(title_contains))
    if genre_ids:
        query = query.where(
            Game.genres.any(Genre.id.in_(genre_ids))
        )
    query = query.order_by(db.desc(Game.id))
    pagination = db.paginate(query, page=page, per_page=per_page)
    return pagination

def create_game(title: str, 
                description: str,
                release_date: datetime,
                cover_path: str = 'defaultcover.jpg',
                platforms: List[Platform] = [],
                genres: List[Genre] = []) -> Game:
    """Создает игру"""
    try:
        game = Game(
            title=title,
            description=description,
            release_date=release_date,
            cover_path=cover_path,
            platforms=platforms,
            genres=genres
        )
        
        db.session.add(game)
        db.session.commit()
        return game
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError(f"Не получилось добавить игру: {e}") from e
    
       
def update_game(
    game_id: int, 
    new_title:str, 
    new_desc: str, 
    new_release_date: datetime, 
    new_platforms: list[Platform], 
    new_genres: list[Genre],
    new_cover: str | None
):
    game: Game = get_item(Game, game_id)
    if not game:
        raise DatabaseNotFoundError(f"Нет такой игры <{game_id}>")
    try:
        game.title = new_title
        game.description = new_desc
        game.release_date = new_release_date
        if new_cover:
            game.cover_path = new_cover
        
        game.platforms = new_platforms
        game.genres = new_genres
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Не получилось обновить игру <{game_id}>: {e}") from e
    
    
def delete_game(game_id: int):
    """Удаление игры"""
    game: Game = get_item(Game, game_id)
    if not game:
        abort(404)
        
    # Сначала удаляем все отзывы у игры
    try:
        db.session.execute(db.delete(Review).where(Review.game_id==game_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseDeleteEntityError(f"Не получилось удалить коментарии пользователя") from e
    
    try:
        # если у игры нестандартная обложка, то её нужно удалить вместе с ней
        if game.cover_path != "defaultcover.jpg":
            delete_image(game.cover_uri)
    except FileDeleteError as e:
        db.session.rollback()
        raise DatabaseDeleteEntityError(f"Не получилось удалить аватарку пользователя") from e

    try:
        db.session.delete(game)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseDeleteEntityError(f"Не получилось удалить пользователя") from e
    
    