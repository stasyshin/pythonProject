from typing import Annotated, List

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.postgres import PostgresClient
from app.repositories.user import UserRepository
from app.schemas.base import ID

from app.schemas.user import UserInfo, UserUpdate,  UserFullInfo

from app.services.exception import ExistsException, NotExistsException

router = APIRouter()

Session = Annotated[AsyncSession, Depends(PostgresClient.get_session)]


@router.post("/user", response_model=ID)
async def add_user(session: Session,
                   update: UserUpdate,
                   ):
    user = await UserRepository.add_user(session,
                                         name=update.name,
                                         description=update.description,
                                         )
    await session.commit()

    if not user:
        raise ExistsException(field="user")

    return {"id": user.id}


@router.get("/user", response_model=List[UserInfo])
async def get_users(session: Session,
                    ):
    users = await UserRepository.get_user(session=session)
    return users


@router.get("/user/{user_id}", response_model=UserFullInfo)
async def get_user(session: Session,
                   user_id: int,
                   ):
    user = await UserRepository.get_user(session=session, user_id=user_id)

    if not user:
        raise NotExistsException(field="user")

    return user


@router.put("/user/{user_id}", response_model=UserUpdate)
async def update_user(session: Annotated[AsyncSession, Depends(PostgresClient.get_session)],
                      user_id: int,
                      update: UserUpdate,
                      ):
    user = await UserRepository.update_user(session=session, user_id=user_id, **update.model_dump())
    await session.commit()

    if not user:
        raise NotExistsException(field="user")

    return user


@router.delete("/user/{user_id}", response_model=ID)
async def delete_user(session: Annotated[AsyncSession, Depends(PostgresClient.get_session)],
                      user_id: int,
                      ):
    user = await UserRepository.delete_user(session=session, user_id=user_id)
    await session.commit()

    if not user:
        raise NotExistsException(field="user")

    return {"id": user.id}
