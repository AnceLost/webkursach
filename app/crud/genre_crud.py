from .base import *

def create_genre(name: str) -> Genre:
    try:
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()   
        return genre 
    except SQLAlchemyError as e:
        db.session.rollback
        raise DatabaseCreateEntityError(f"Не получилось добавить жанр: {e}") from e
    
def edit_genre(genre_id: int, new_name:str):
    try:
        genre: Genre = get_item(Genre, genre_id)
        if not genre:
            raise DatabaseNotFoundError(f"Не нашлось жанра <{genre_id}>")
        genre.name = new_name
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Не удалось обновить название жанра: {e}") from e