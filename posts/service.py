
from .repository import PostRepository
from .client import PostResponse, PostCreate, PostUpdate

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def findAll(self) -> list[PostResponse]:
        posts = self.repository.find_all()
        return [PostResponse.model_validate(post) for post in posts]

    def findById(self, id: int) -> PostResponse:
        post = self.repository.find_by_id(id)
        return PostResponse.model_validate(post)

    def create(self, post: PostCreate) -> PostResponse:
        new_post = self.repository.create(post)
        return PostResponse.model_validate(new_post)

    def update(self, post: PostUpdate) -> PostResponse:
        update_post = self.repository.update(post)
        return PostResponse.model_validate(update_post)

    def delete(self, id: int) -> bool:
        return self.repository.delete(id)
    