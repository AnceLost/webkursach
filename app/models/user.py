from .base import *
    
class User(Base, UserMixin):
    __tablename__ = 'users'
    
    id: Mapped[intpk]
    login: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    avatar_path: Mapped[str] = mapped_column(String(256), nullable=True, server_default="defaultavatar.jpg")
    password_hash: Mapped[str] = mapped_column(String(256))
    nickname: Mapped[str] = mapped_column(String(50)) #Это имя будет видно другим пользователям
    banned: Mapped[bool] = mapped_column(default=False, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("userroles.id"))
    role: Mapped["UserRole"] = relationship()
    reviews: Mapped[List["Review"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    created_at: Mapped[createdAt]
    updated_at: Mapped[updatedAt]
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
    
    @property
    def avatar_uri(self):
        return url_for('static', filename=f'upload/avatars/{self.avatar_path}')
