from .base import *

# платформа в смысле ОС или устройство, на которой можно запустить игру
class Platform(Base):
    __tablename__ = 'platforms'
    
    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(200))