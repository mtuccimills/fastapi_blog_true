from .client import PostCreate, PostUpdate, PostResponse
from .service import PostService
from .repository import PostRepository
from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
from directories import templates

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)


@router.get("/", response_class=HTMLResponse)
def get_posts(request: Request, service: PostService = Depends(get_service)):
    posts = service.findAll()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"posts": posts}
    )


@router.get("/post/{id}", response_class=HTMLResponse)
def find_by_id(id: int, request: Request, service: PostService = Depends(get_service)):
    post = service.findById(id)
    return templates.TemplateResponse(
        request,
        "post.html",
        {"post": post}
    )


@router.get("/post/create", response_class=HTMLResponse)
def create_post_form(request: Request):
    return templates.TemplateResponse(request, "create_post.html", {})


@router.post("/post/create", response_class=HTMLResponse)
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    user_id: int = Form(...),
    service: PostService = Depends(get_service),
):
    post = PostCreate(title=title, content=content, user_id=user_id)
    service.create(post)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
