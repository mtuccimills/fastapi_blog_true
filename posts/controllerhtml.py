from directories import templates
from .service import PostService
from .repository import PostRepository
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from db import get_db

# Controlador de usuarios, que funciona como capa de contacto con el exterior. Resuelve Requests y devuelve Responses.
# Maneja JSON Validator, SWAGGER, Auth.
router = APIRouter()
# Iniciamos la vida de la conexión a la base de datos desde que llega la conexión, auqnue no la usemos hasta que lleguemos al controlador.
def get_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository) # db -> repository -> service

@router.get("/posts"
         , include_in_schema= False
         , name="posts"
         )
@router.get("/"
         , include_in_schema= False
         , name="home"
         )
def home(request: Request, service: PostService = Depends(get_service)):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": service.findAll(), "title": "Home"} # Sent information to the view
    )

@router.get("/posts/{id}",
            include_in_schema= False
            )#, response_model=Post | None)
def post_page(request: Request, id: int, service: PostService = Depends(get_service)):
    post = service.findById(id) 
    return templates.TemplateResponse(
        request,
        "post.html",
        {"post": post, "title": f"Post - {post.title[:50]}"} # Sent information to the view
    )
