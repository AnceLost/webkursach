from .base import *

def get_self_review(user_id, game_id) -> Review | None:
    return db.select(Review).filter(user_id=user_id, game_id=game_id).first()

def average_rating_for_game(game_id: int) -> float:
    res = db.session.query(db.func.avg(Review.mark)).filter(Review.game_id==game_id).scalar()
    return res

def create_review(mark: int, content: str, user_id: int, game_id: int) -> Review | None:
    try:
        review = Review(
            mark=mark,
            content=content,
            user_id=user_id,
            game_id=game_id
        )
        db.session.add(review)
        db.session.commit()
        return review
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError(f"Не удалось создать коментарий: {e}")
        