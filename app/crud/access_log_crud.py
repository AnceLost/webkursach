from .base import *

def get_access_logs_time_desc(page=1, per_page=100, limit=100):
    stmt = db.select(AccessLog).order_by(AccessLog.timestamp.desc()).limit(limit)
    pag = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return pag

def create_access_log(user_id: int, ip_address: str) -> AccessLog:
    try:
        log = AccessLog(user_id=user_id, ip_address=ip_address)
        db.session.add(log)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise DatabaseCreateEntityError(f"Не получилось зарегистрировать журнал: {e}") from e
    