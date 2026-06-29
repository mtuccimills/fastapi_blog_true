from .client import PostResponse, PostCreate, PostUpdate
from .service import PostService
from .repository import PostRepository
from fastapi import APIRouter, status, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db

# Controlador de usuarios, que funciona como capa de contacto con el exterior. Resuelve Requests y devuelve Responses.
# Aquí genero la sesión de la base de datos para poder manejarla a lo largo de todo el proceso, auqnue solo se use en el controlador
# Maneja JSON Validator, SWAGGER, Auth.
router = APIRouter()
# Iniciamos la vida de la conexión a la base de datos desde que llega la conexión, auqnue no la usemos hasta que lleguemos al controlador.
def get_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository) # db -> repository -> service

@router.get("/", response_model=list[PostResponse])
def get_posts(service: PostService = Depends(get_service)):
    posts = service.findAll()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
    return posts
@router.get("/{id}", response_model=PostResponse)
def find_by_id(id: int, service: PostService = Depends(get_service)):
    return service.findById(id)

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, service: PostService = Depends(get_service)):
    return service.create(post)

@router.put("/", response_model=PostResponse)
def update_post(post: PostUpdate, service: PostService = Depends(get_service)):
    return service.update(post)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, service: PostService = Depends(get_service)):
    return service.delete(id)


