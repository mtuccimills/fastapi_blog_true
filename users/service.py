from .repository import UserRepository
from .client import UserResponse, UserCreate, UserUpdate
from posts.client import PostResponse
from fastapi import HTTPException, status

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def find_all(self) -> list[UserResponse]:
        users = await self.repository.find_all()
        return [UserResponse.model_validate(user) for user in users]

    async def find_by_id(self, id: int) -> UserResponse:
        user = await self.repository.find_by_id(id)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found"
        )

    async def find_by_email(self, email: str) -> UserResponse:
        user = await self.repository.find_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with email {email} not found"
        )

    async def find_by_username(self, username: str) -> UserResponse:
        user = await self.repository.find_by_username(username)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with username {username} not found"
        )

    async def create(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.repository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} already exists",
            )

        existing_user = await self.repository.find_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} already exists",
            )

        new_user = await self.repository.create(user_data)
        return UserResponse.model_validate(new_user)

    async def update_full(self, user_id: int, user_data: UserCreate) -> UserResponse:
        existing_user = self.find_by_id(user_id)
        existing_user = await self.repository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} not available",
            )
        existing_user = await self.repository.find_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} not available",
            )
        
        update_user = await self.repository.update_full(user_id, user_data)
        return UserResponse.model_validate(update_user)

    async def update_partial(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        existing_user = self.find_by_id(user_id)
        if not existing_user:  # add this check
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} not found",
            )
        existing_user = await self.repository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} not available",
            )
        existing_user = await self.repository.find_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} not available",
            )
        
        update_user = await self.repository.update_partial(user_id, user_data)
        return UserResponse.model_validate(update_user)

    async def delete(self, id: int) -> bool:
        user = await self.repository.find_by_id(id)
        if user:
            return self.repository.delete(user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    
    async def get_posts(self, id:int) -> list[PostResponse]:        
        user = await self.repository.find_by_id(id)
        if user:
            posts = await self.repository.get_posts(user.id)
            return [PostResponse.model_validate(post) for post in posts]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    