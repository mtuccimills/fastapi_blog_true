from .service import UserService
from .repository import UserRepository
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db import get_db

from directories import templates

# Controlador de usuarios, que funciona como capa de contacto con el exterior. Resuelve Requests y devuelve Responses.
# Maneja JSON Validator, SWAGGER, Auth.
router = APIRouter()
# Iniciamos la vida de la conexión a la base de datos desde que llega la conexión, auqnue no la usemos hasta que lleguemos al controlador.
def get_service(db:Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

@router.get("/{user_id}/posts",
            include_in_schema= False,
            name="user_posts"
            )#, response_model=Post | None)
def user_page(request: Request, user_id: int, service: UserService = Depends(get_service)):
    user = service.find_by_id(user_id) 
    posts = service.get_posts(user_id) 
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"User - {user.username[:20]}'s Post"} # Sent information to the view
    )
