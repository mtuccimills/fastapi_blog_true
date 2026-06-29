from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "My first post",
                "content": "Content example of a post",
                "author": "Matias Tucci",
                "date_posted": "2023-01-01",
            }
        }
    )


class PostCreate(PostBase):
    user_id: int


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "title": "My NEW first post",
            }
        }
    )


class PostResponse(PostBase):
    id: int
    user_id: int
    author: str
    date_posted: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "10",
                "title": "My first post",
                "content": "Content example of a post",
                "author": "Matias Tucci",
                "date_posted": "2023-01-01",
                "user_id": "1",
            }
        }
    )
