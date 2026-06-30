from sqlalchemy import select
#from sqlalchemy.ext.asyncio import AsyncSession
#from model import Post
from .client import UserCreate, UserUpdate, UserResponse
import models
# 7 async
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload #, Session

class UserRepository:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def find_all(self) -> list[models.User]:
        result = await self.db.execute(select(models.User).options(selectinload(models.User.posts)))
        db_users = result.scalars().all()
        return db_users
        
    async def find_by_id(self, id: int) -> models.User | None:
        result = await self.db.execute(select(models.User).where(models.User.id == id).options(selectinload(models.User.posts)))
        db_user = result.scalars().first()
        return db_user
        

    async def find_by_email(self, email: str) -> models.User | None:
        result = await self.db.execute(select(models.User).where(models.User.email == email).options(selectinload(models.User.posts)))
        return result.scalars().first()  # just returns None if not found


    async def find_by_username(self, username: str) -> models.User | None:
        result = await self.db.execute(select(models.User).where(models.User.username == username).options(selectinload(models.User.posts)))
        return result.scalars().first()

    async def create(self, user: UserCreate) -> models.User:
        new_user = models.User(
            username=user.username,
            email=user.email
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user, attribute_names=["posts"])
        return new_user

    async def update_full(self, user_id: int, user_data: UserResponse) -> models.User:
        db_user = await self.find_by_id(user_id)
        db_user.username = user_data.username
        db_user.email = user_data.email
        await self.db.commit()
        await self.db.refresh(db_user, attribute_names=["posts"])
        return db_user

    async def update_partial(self,user_id:int, user_data: UserUpdate) -> models.User:
        db_user = await self.find_by_id(user_id)

        # Update Logic
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        # # Manual update
        # if user_data.username is not None:
        #     db_user.username = user_data.username
        # if user_data.email is not None:
        #     db_user.email = user_data.email
        # if user_data.image_file is not None:
        #     db_user.image_file = user_data.image_file

        await self.db.commit()
        await self.db.refresh(db_user, attribute_names=["posts"])
        return db_user

    async def delete(self, id: int) -> bool:
        db_user = await self.find_by_id(id)
        self.db.delete(db_user)
        await self.db.commit()
        return True
        
    async def get_posts(self, id: int) -> list[models.Post]:
        user = await self.find_by_id(id)
        return user.posts
        
