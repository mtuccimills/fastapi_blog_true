from .client import UserResponse, UserCreate, UserUpdate
from .service import UserService
from .repository import UserRepository
from posts.client import PostResponse
from fastapi import APIRouter, Depends, HTTPException, status
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
#from db import get_db
from db import get_async_db

# Controlador de usuarios, que funciona como capa de contacto con el exterior. Resuelve Requests y devuelve Responses.
# Maneja JSON Validator, SWAGGER, Auth.
router = APIRouter()
# Iniciamos la vida de la conexión a la base de datos desde que llega la conexión, auqnue no la usemos hasta que lleguemos al controlador.
async def get_service(db:AsyncSession = Depends(get_async_db)) -> UserService:
    repository = await UserRepository(db)
    return await UserService(repository)

@router.get("/", response_model=list[UserResponse])
async def get_users(service: UserService = Depends(get_service)):
    users = await service.find_all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    return users

@router.get("/email/{email}", response_model=UserResponse)
async def find_by_email(email: str, service: UserService = Depends(get_service)):
    return await service.find_by_email(email)

@router.get("/username/{username}", response_model=UserResponse)
async def find_by_username(username: str, service: UserService = Depends(get_service)):
    return await service.find_by_username(username)

@router.get("/{id}/posts", response_model=list[PostResponse])
async def get_posts(id: int, service: UserService = Depends(get_service)):
    return await service.get_posts(id)

@router.get("/{id}", response_model=UserResponse)
async def find_user_by_id(id: int, service: UserService = Depends(get_service)):
    return await service.find_by_id(id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(user: UserCreate, service: UserService = Depends(get_service)):
    return await service.create(user)

@router.put("/", response_model=UserResponse)
async def update_full(user_id: int,user: UserCreate, service: UserService = Depends(get_service)):
    return await service.update_full(user_id,user)

@router.patch("/", response_model=UserResponse)
async def update_partial(user_id: int, user: UserUpdate, service: UserService = Depends(get_service)):
    return await service.update_partial(user_id,user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: UserService = Depends(get_service)):
    return await service.delete(id)


