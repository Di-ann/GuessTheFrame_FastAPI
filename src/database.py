from datetime import datetime
from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from src.core.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'