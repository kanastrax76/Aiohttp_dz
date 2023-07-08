from typing import Type
from cachetools import cached
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import EmailType

import config

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)


class Advertisement(Base):

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    description = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


@cached({})
def get_engine():
    return create_async_engine(config.PG_DSN)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine(), expire_on_commit=False, class_=AsyncSession)


async def init_db(conn):
    await conn.run_sync(Base.metadata.create_all)


ORM_MODEL_CLS = Type[User] | Type[Advertisement]
ORM_MODEL = User | Advertisement
