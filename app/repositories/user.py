
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User
from app.services.exception import exception_decorator


class UserRepository:
    @staticmethod
    @exception_decorator
    async def add_user(session: AsyncSession, *,
                       name: str,
                       description: str,
                       ):
        stmt = (
            insert(User).
            values(name=name,
                   description=description,
                   )
        )
        stmt = (stmt.
                returning(User.id)
                )

        return (await session.execute(stmt)).mappings().one_or_none()

    @staticmethod
    @exception_decorator
    async def get_user(session: AsyncSession, *,
                       user_id: int = None):
        stmt = (
            select(User.id,
                   User.name,
                   User.description,
                   User.date_create,
                   User.date_update,
                   )
        )
        if user_id:
            stmt = stmt.where(User.id == user_id)
            return (await session.execute(stmt)).mappings().one_or_none()

        return (await session.execute(stmt)).mappings().all()

    @staticmethod
    @exception_decorator
    async def update_user(session: AsyncSession, *,
                          user_id: int,
                          name: str,
                          description: str,
                          ):

        stmt = (
            update(User).
            where(User.id == user_id).
            values(
                   name=name,
                   description=description,
                   )
        )

        stmt = stmt.returning(User.id,
                              User.name,
                              User.description,
                              )
        return (await session.execute(stmt)).mappings().one_or_none()

    @staticmethod
    @exception_decorator
    async def delete_user(session: AsyncSession, *,
                          user_id: int):
        stmt = (
            delete(User).
            where(User.id == user_id).
            returning(User.id)
        )
        return (await session.execute(stmt)).mappings().one_or_none()
