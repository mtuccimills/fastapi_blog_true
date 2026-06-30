from sqlalchemy import select
#from sqlalchemy.ext.asyncio import AsyncSession
#from model import Post
from .client import PostCreate, PostUpdate
from fastapi import HTTPException, status
import models
# 7 async
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload #, Session

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(self) -> list[models.Post]:
        result = await self.db.execute(select(models.Post).options(selectinload(models.Post.author)))
        db_posts = result.scalars().all()
        return db_posts
        
    async def find_by_id(self, id: int) -> models.Post | None:
        result = await self.db.execute(select(models.Post).where(models.Post.id == id).options(selectinload(models.Post.author)))
        db_post = result.scalars().first()
        if db_post:
            return db_post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Post with id {id} not found"
        )

    async def create(self, post: PostCreate) -> models.Post:
        result = await self.db.execute(select(models.User).where(models.User.id == post.user_id).options(selectinload(models.User.posts)))
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail = f"User with id {post.user_id} not found"
            )
        
        new_db_post = models.Post(
            title=post.title,
            content=post.content,
            user_id=post.user_id
        )
        self.db.add(new_db_post)
        await self.db.commit()
        await self.db.refresh(new_db_post, attribute_names=["author"])
        return new_db_post

    async def update_full(self, post_id: int, post_data: PostCreate) -> models.Post:
        db_post = await self.find_by_id(post_id)
        db_post.title = post_data.title
        db_post.content = post_data.content
        db_post.user_id = post_data.user_id
        await self.db.commit()
        await self.db.refresh(db_post, attribute_names=["author"])
        return db_post

    async def update_partial(self, post_id: int, post_data: PostUpdate) -> models.Post:
        db_post = await self.find_by_id(post_id)
        update_date = post_data.model_dump(exclude_unset=True)
        for field, value in update_date.items():
            setattr(db_post, field, value)
        await self.db.commit()
        await self.db.refresh(db_post, attribute_names=["author"])
        return db_post

    async def delete(self, id: int) -> bool:
        db_post = self.find_by_id(id)
        self.db.delete(db_post)
        await self.db.commit()
        return True
