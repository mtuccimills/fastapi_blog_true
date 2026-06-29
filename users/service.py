from .repository import UserRepository
from .client import UserResponse, UserCreate, UserUpdate
from posts.client import PostResponse
from fastapi import HTTPException, status

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def find_all(self) -> list[UserResponse]:
        users = self.repository.find_all()
        return [UserResponse.model_validate(user) for user in users]

    def find_by_id(self, id: int) -> UserResponse:
        user = self.repository.find_by_id(id)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id {id} not found"
        )

    def find_by_email(self, email: str) -> UserResponse:
        user = self.repository.find_by_email(email)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with email {email} not found"
        )

    def find_by_username(self, username: str) -> UserResponse:
        user = self.repository.find_by_username(username)
        if user:
            return UserResponse.model_validate(user)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with username {username} not found"
        )

    def create(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.repository.find_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} already exists",
            )

        existing_user = self.repository.find_by_username(user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} already exists",
            )

        new_user = self.repository.create(user_data)
        return UserResponse.model_validate(new_user)

    def update(self, user_data: UserUpdate) -> UserResponse:
        existing_user = self.repository.find_by_id(user_data.id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Id {user_data.id} not found",
            )

        existing_user = self.repository.find_by_email(user_data.email)
        if existing_user and existing_user.id != user_data.id:  # add this check
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {user_data.email} already exists",
            )

        existing_user = self.repository.find_by_username(user_data.username)
        if existing_user and existing_user.id != user_data.id:  # add this check
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username {user_data.username} already exists",
            )

        update_user = self.repository.update(user_data)
        return UserResponse.model_validate(update_user)

    def delete(self, id: int) -> bool:
        user = self.repository.find_by_id(id)
        if user:
            return self.repository.delete(user.id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    
    def get_posts(self, id:int) -> list[PostResponse]:        
        user = self.repository.find_by_id(id)
        if user:
            posts = self.repository.get_posts(user.id)
            return [PostResponse.model_validate(post) for post in posts]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    