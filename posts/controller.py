from .client import PostResponse, PostCreate, PostUpdate
from .service import PostService
from .repository import PostRepository
from fastapi import APIRouter, status, Depends, HTTPException, status
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
#from db import get_db
from db import get_async_db

# Controlador de usuarios, que funciona como capa de contacto con el exterior. Resuelve Requests y devuelve Responses.
# Aquí genero la sesión de la base de datos para poder manejarla a lo largo de todo el proceso, auqnue solo se use en el controlador
# Maneja JSON Validator, SWAGGER, Auth.
router = APIRouter()
# Iniciamos la vida de la conexión a la base de datos desde que llega la conexión, auqnue no la usemos hasta que lleguemos al controlador.
def get_service(db: AsyncSession = Depends(get_async_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository) # db -> repository -> service

@router.get("/", response_model=list[PostResponse])
async def get_posts(service: PostService = Depends(get_service)):
    posts = await service.findAll()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
    return posts
@router.get("/{id}", response_model=PostResponse)
async def find_by_id(id: int, service: PostService = Depends(get_service)):
    return await service.findById(id)

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, service: PostService = Depends(get_service)):
    return await service.create(post)

@router.put("/", response_model=PostResponse)
async def update_post(post_id: int,post: PostCreate, service: PostService = Depends(get_service)):
    return await service.update_full(post_id, post)

@router.patch("/", response_model=PostResponse)
async def update_post(post_id: int,post: PostUpdate, service: PostService = Depends(get_service)):
    return await service.update_partial(post_id, post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, service: PostService = Depends(get_service)):
    return await service.delete(id)


