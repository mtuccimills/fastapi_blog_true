
from .repository import PostRepository
from .client import PostResponse, PostCreate, PostUpdate

class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def findAll(self) -> list[PostResponse]:
        posts = await self.repository.find_all()
        return [PostResponse.model_validate(post) for post in posts]

    async def find_all_raw(self) -> list[models.Post]:
        return await self.repository.find_all()

    async def findById(self, id: int) -> PostResponse:
        post = await self.repository.find_by_id(id)
        return PostResponse.model_validate(post)

    async def find_by_id_raw(self, id: int) -> models.Post | None:
        return await self.repository.find_by_id(id)

    async def create(self, post: PostCreate) -> PostResponse:
        new_post = await self.repository.create(post)
        return PostResponse.model_validate(new_post)

    async def update_full(self, post_id: int, post: PostCreate) -> PostResponse:
        update_post = await self.repository.update_full(post_id, post)
        return PostResponse.model_validate(update_post)

    async def update_partial(self, post_id: int, post: PostUpdate) -> PostResponse:
        update_post = await self.repository.update_partial(post_id, post)
        return PostResponse.model_validate(update_post)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)
    
