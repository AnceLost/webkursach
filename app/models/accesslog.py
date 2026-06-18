from .base import *

class AccessLog(Base):
    __tablename__ = 'access_log'
    id: Mapped[intpk]
    
    ip_address = mapped_column(String(45), nullable=False)
    timestamp: Mapped[createdAt]
    
    user_id = mapped_column(ForeignKey('users.id'), nullable=True)  # для гостей может быть NULL
    user = relationship('User', backref='access_logs')