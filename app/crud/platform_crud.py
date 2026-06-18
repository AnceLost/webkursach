from .base import *

def create_platform(name: str) -> Platform:
    try:
        platform = Platform(name=name)
        db.session.add(platform)
        db.session.commit()
        return platform    
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError(f"Не получилось добавить платформу: {e}") from e
    
def edit_platform(platform_id: int, new_name:str):
    try:
        platform: Platform = get_item(Platform, platform_id)
        if not platform:
            raise DatabaseNotFoundError(f"Не нашлось платформы <{platform_id}>")
        platform.name = new_name
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Не удалось обновить название платформы: {e}") from e
     
    
    