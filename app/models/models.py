
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, func, ForeignKey, UniqueConstraint, BigInteger
)

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer(), primary_key=True, nullable=False, autoincrement=True)
    name = Column("name", String(length=50), nullable=False, unique=True)
    description = Column("description", String(length=100), nullable=False)
    date_create = Column("date_create", DateTime(), server_default=func.now())
    date_update = Column("date_update", DateTime(), onupdate=func.now())





