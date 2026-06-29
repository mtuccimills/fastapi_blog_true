<<<<<<< HEAD
from datetime import datetime 
from pydantic import BaseModel, Field
from users.client import UserResponse


# Entidade de los modelos de datos a utilizar en el proyecto.
# Consumir fuente de información externa.

from pydantic import BaseModel, ConfigDict, Field
=======
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

>>>>>>> 759d8f44408be76c01af4594ba217c5022bd4cc0

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

<<<<<<< HEAD
    model_config = {
        "from_attributes": True,
        "populate_by_name": True, 
        "json_schema_extra":{
            "example": {
                "title": "My first post",
                "content": "Content example of a post",
                "user_id": "1"
            }
        }
    }

class PostCreate(PostBase):
    user_id: int # TEMPORARY
    pass

class PostUpdate(PostBase):
    user_id: int # TEMPORARY
    id: int
    pass


class PostResponse(PostBase):
=======
>>>>>>> 759d8f44408be76c01af4594ba217c5022bd4cc0
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
<<<<<<< HEAD
                "id": 1,
=======
>>>>>>> 759d8f44408be76c01af4594ba217c5022bd4cc0
                "title": "My first post",
                "content": "Content example of a post",
                "author": "Matias Tucci",
                "date_posted": "2023-01-01",
<<<<<<< HEAD
                "user_id": "10",
=======
>>>>>>> 759d8f44408be76c01af4594ba217c5022bd4cc0
            }
        }
    )

<<<<<<< HEAD
    id: int
    user_id:int
    date_posted:datetime
    author: UserResponse

    

    
    
# class User(BaseModel):
#     id: int
#     name: str = Field(min_length=1, max_length=50, alias="username")
#     email: EmailStr = Field(max_length=120)
#     password: str = Field(min_length=8, max_length=20, alias="password_hash")
#     postalCode: int | None = Field(default=None, ge=10000,le=999999)

#     # Configuración adicional para el modelo, como ejemplos para la documentación de la API.
#     model_config = {
#         "from_attributes": True,
#         "populate_by_name": True, 
#         "json_schema_extra":{
#             "example": {
#                 "id": 1,
#                 "name": "Matias",
#                 "email": "matias@gmail.com",
#                 "password": "asdfaseqwwqdwqdsa",
#                 "postalCode": 38556
#             }
#         }
#     }


=======

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
>>>>>>> 759d8f44408be76c01af4594ba217c5022bd4cc0
