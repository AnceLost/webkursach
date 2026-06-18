from .base import *

def get_self_review(user_id, game_id) -> Review | None:
    return db.session.query(Review).filter_by(user_id=user_id, game_id=game_id).first()

def get_pagination_reviews_for_games(game_id: int, page=1, per_page=5):
    reviews = db.select(Review).filter(Review.game_id==game_id)
    pagination = db.paginate(reviews, page=page, per_page=per_page)
    return pagination

def get_reviews_with_game(user_id):
    """Возвращает все отзывы пользователя с подгрузкой игры"""
    return db.session.query(Review)\
        .filter(Review.user_id == user_id)\
        .options(
            db.joinedload(Review.game)
            .joinedload(Game.platforms),
            db.joinedload(Review.game)
            .joinedload(Game.genres))\
        .order_by(Review.mark.desc())\
        .all()

def create_review(mark: int, content: str, user_id: int, game_id: int) -> Review | None:
    try:
        review = Review(
            mark=mark,
            text=content,
            user_id=user_id,
            game_id=game_id
        )
        db.session.add(review)
        db.session.commit()
        return review
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError(f"Не удалось создать коментарий: {e}") from e
    
