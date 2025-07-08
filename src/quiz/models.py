from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, Enum, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from sqlalchemy import Enum as SQLEnum
import enum
from src.auth.models import User

class MediaType(str, enum.Enum):
    MOVIE = "movie"
    SERIES = "series"
    ANIME = "anime"
    OTHER = "other"


class MediaItem(Base):
    title: Mapped[str] = mapped_column(String(255), nullable=False)  
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)  
    type: Mapped[MediaType] = mapped_column(default=MediaType.OTHER, server_default=text("'OTHER'"))  
    genre: Mapped[str] = mapped_column(String(100), nullable=True)  
    difficulty: Mapped[int] = mapped_column(Integer, default=1) 
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user_answers = relationship("UserAnswer", back_populates="media_item", cascade="all, delete-orphan")


class UserAnswer(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    media_item_id: Mapped[int] = mapped_column(ForeignKey("mediaitems.id", ondelete="CASCADE"), nullable=False)
    answer: Mapped[str] = mapped_column(String(255), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="answers")
    media_item = relationship("MediaItem", back_populates="user_answers")



