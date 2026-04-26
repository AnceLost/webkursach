from datetime import datetime

from .base import *

def get_game(game_id) -> Game | None:
    """Возвращает игру по ID или None."""
    return db.session.get(Game, game_id)

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
    return pagination.items

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
            release_date=release_date.date(),
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
    

def update_game(game_id: int,
                new_title: str = None,
                new_description: str = None,
                new_release_date: datetime = None,
                new_platforms: List[Platform] = None,
                new_genres: List[Genre] = None):
    """
    Обновляет поля модели игры
    :param new_platforms: Сразу составляйте полный список, потому что идет замена
    :param new_genres: Сразу составляйте полный список, потому что идет замена
    """
    try:
        game = get_game(game_id)
        if game:
            if new_title: game.title = new_title
            if new_description: game.description = new_description
            if new_release_date: game.release_date = new_release_date
            if new_platforms: game.platforms = new_platforms
            if new_genres: game.genres = new_genres
        else:
            raise DatabaseNotFoundError(f"Нет игры с {game_id=}")
        
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Не получилось обновить игру: {e}") from e

def update_game_cover(game_id: int, new_cover):
    try: 
        game = get_game(game_id)
        if new_cover and game:
            game.cover_path = new_cover
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Ошибка БД при обновлении обложки у игры: {e}") from e
    
    
def delete_game(game_id):
    """Удаляет игру по id"""
    try:
        game = get_game(game_id)
        db.session.delete(game)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseDeleteEntityError(f"Не удалось удалить игру: {e}") from e
    