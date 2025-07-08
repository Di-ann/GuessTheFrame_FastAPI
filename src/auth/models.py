from sqlalchemy import Boolean, DateTime, func
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] 
    score: Mapped[int] = mapped_column(nullable=False, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    answers = relationship("UserAnswer", back_populates="user", cascade="all, delete-orphan")