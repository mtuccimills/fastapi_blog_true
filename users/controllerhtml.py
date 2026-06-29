from .client import UserCreate, UserUpdate, UserResponse
from .service import UserService
from .repository import UserRepository
from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
from directories import templates

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)


@router.get("/", response_class=HTMLResponse)
def get_users(request: Request, service: UserService = Depends(get_service)):
    users = service.find_all()
    return templates.TemplateResponse(
        request,
        "users/index.html",
        {"users": users}
    )


@router.get("/{id}", response_class=HTMLResponse)
def find_user_by_id(id: int, request: Request, service: UserService = Depends(get_service)):
    user = service.find_by_id(id)
    return templates.TemplateResponse(
        request,
        "users/profile.html",
        {"user": user}
    )


@router.get("/create", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse(request, "users/create.html", {})


@router.post("/create", response_class=HTMLResponse)
def create_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    service: UserService = Depends(get_service),
):
    user = UserCreate(username=username, email=email)
    service.create(user)
    return RedirectResponse(url="/users", status_code=status.HTTP_303_SEE_OTHER)
