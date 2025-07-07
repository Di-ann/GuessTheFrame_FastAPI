from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] 
    score: Mapped[int] = mapped_column(nullable=False, default=0)

    answers = relationship("UserAnswer", back_populates="user", cascade="all, delete-orphan")