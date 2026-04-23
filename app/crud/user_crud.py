from .base import *


def get_user(user_id: int) -> User | None:
    """Возвращает пользователя по ID или None."""
    return db.session.get(User, user_id)

def get_user_by_login(login: str) -> User | None:
    """Возвращает пользователя по login"""
    return db.session.execute(
        db.select(User).where(User.login == login)
    ).scalar_one_or_none()
    
def get_users(page: int = 1, per_page: int = 20) -> list[User]:
    """Возвращает список пользователей"""
    users = db.select(User).order_by(User.id)
    pagination = db.paginate(users, page=page, per_page=per_page)
    return pagination.items

def get_user_by_email(email: str):
    """Возвращает пользователя по email"""
    return db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

def search_users(login_contains: str = None, role_id: int = None, limit: int = 10) -> list[User]:
    """Поиск пользователей по логину, роли"""
    query = db.select(User)
    if login_contains:
        query = query.where(User.login.contains(login_contains))
    if role_id:
        query = query.where(User.role_id == role_id)
    query = query.order_by(db.desc(User.id)).limit(limit)
    return db.session.execute(query).scalars().all()

def create_user(login: str, password: str, nickname: str, email: str, role_id: int = 1) -> User:
    """Функция для создания пользователя (пользователь роль не выбирает)"""
    try:
        user = User(
            login=login,
            nickname=nickname,
            email=email,
            role_id=role_id
        )
        user.set_password(password=password)
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError("Не получилось создать пользователя или добавить его в базу") from e
    
    return user

def update_user(user_id: int, #обязательный
                new_password: str | None = None, 
                new_nickname: str | None = None,
                new_email: str | None = None,
                new_role_id: int | None = None,) -> User | None:
    """Обновляет пользователя """
    user = get_user(user_id)
    if(user):
        if new_password: user.set_password(new_password)
        if new_email: user.email = new_email
        if new_nickname: user.nickname = new_nickname
        if new_role_id: user.role_id = new_role_id
    else:
        raise DatabaseNotFoundError("Вы пытаетесь изменить несуществующего пользователя")
    try:
        db.session.commit()
        return user
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError("Не получилось изменить пользователя") from e

def update_user_avatar(user_id: int, new_avatar_path: str):
    try: 
        user = get_user(user_id)
        if new_avatar_path and user:
            user.avatar_path = new_avatar_path
            db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseUpdateError(f"Ошибка БД при обновлении аватара: {e}") from e

def delete_user(user_id: int):
    """Удаление пользователя"""
    user = get_user(user_id)
    db.session.delete(user)
    db.session.commit()
    
