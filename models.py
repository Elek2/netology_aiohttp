from datetime import datetime
from config import DB_DSN
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker


DB_DSN = "sqlite+aiosqlite:///test.db"  # для тестовой базы данных sqlite

engine = create_async_engine(DB_DSN)  # создание асинхронного движка
Base = declarative_base()  # создание БД
Session = sessionmaker(bind=engine, class_=AsyncSession)  # сессия для асинхронного движка


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    advertisements = relationship("Advertisement", back_populates="users")


class Advertisement(Base):
    __tablename__ = "advertisements"
    id = Column(Integer, primary_key=True)
    header = Column(String(100), nullable=False)
    description = Column(String(100))
    created_on = Column(DateTime(), default=datetime.now)
    author_id = Column(ForeignKey("users.id"), nullable=False)
    users = relationship("User", back_populates="advertisements")
