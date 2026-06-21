from sqlalchemy.exc import SQLAlchemyError
from typing import TypeVar, Optional, List

from app.dbhelper import db, Base
from app.models import User, Game, Genre, Platform, Review, AccessLog
from app.exceptions import (DatabaseUpdateError, 
                            DatabaseNotFoundError, 
                            DatabaseCreateEntityError, 
                            DatabaseDeleteEntityError,
                            DatabaseError,
                            FileDeleteError,
                            FileSaveError)

T = TypeVar('T', bound=Base)

def get_item(model: type[T], item_id: int) -> Optional[T]:
    """Возвращает экземпляр модели model с указанным id или None."""
    return db.session.get(model, item_id)

def get_items(model: type[T], page: int = 1, per_page: int = 20) -> List[T]:
    """
    Возвращает список объектов с пагинацией
    :param page: номер страницы
    :param per_page: сколько объектов на одной странице
    """
    return get_pagination(model=model, page=page, per_page=per_page).items

def get_pagination(model: type[T], page: int = 1, per_page: int = 20):
    """Возвращает сам объект пагинации
    :param page: номер страницы
    :param per_page: сколько объектов на одной странице
    """
    items = db.select(model).order_by(model.id)
    pagination = db.paginate(items, page=page, per_page=per_page)
    return pagination

def get_items_by_ids(model: type[T], ids: List[int]) -> List[T]:
    """Возвращает список объектов модели model с id, входящими в ids."""
    if not ids: return []
    return db.session.query(model).filter(model.id.in_(ids)).all()

def delete_item(model: type[T], item_id: int):
    try:
        item = get_item(model, item_id)
        db.session.delete(item)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseDeleteEntityError(f"Не удалось удалить объект модели<{model}>: {e}") from e