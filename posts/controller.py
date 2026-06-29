from .client import PostCreate, PostUpdate, PostResponse
from .service import PostService
from .repository import PostRepository
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> PostService:
    repository = PostRepository(db)
    return PostService(repository)


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
def update_post_full(post_id: int, post: PostCreate, service: PostService = Depends(get_service)):
    return service.update_full(post_id, post)


@router.patch("/", response_model=PostResponse)
def update_post_partial(post_id: int, post: PostUpdate, service: PostService = Depends(get_service)):
    return service.update_partial(post_id, post)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, service: PostService = Depends(get_service)):
    return service.delete(id)
