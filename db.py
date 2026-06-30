from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db" # WHere to connect, for sql is here '.' is the current directory while /blog.db is the db name
SQLALCHEMY_ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./blog.db" # WHere to connect, for sql is here '.' is the current directory while /blog.db is the db name

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}, # sqllite specific because it only allows one thread.
)

async_engine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    connect_args={"check_same_thread": False}, # sqllite specific because it only allows one thread.
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
        engine ,
        class_= AsyncSession,
        expire_on_commit=False
    )


class Base(DeclarativeBase):
    pass


def get_db():
    with SessionLocal() as session:
        yield session

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
