from .base import *

class UserRole(Base):
    __tablename__ = 'userroles'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[int] = mapped_column(default=0) #Что-то типа уровня допуска