from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Entidade de los modelos de datos a utilizar en el proyecto.
# Consumir fuente de información externa.

class UserBase(BaseModel):
    username: str = Field(min_length=1,max_length=50)
    email: EmailStr = Field(max_length=120) # EmailStr validates that is not empty
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "username": "Mat",
                "email": "mat@gmail.com",
            }
        }
    )

class UserCreate(UserBase):
    # Add password for authentication
    pass

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120) # EmailStr validates that is not empty
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "username": "Matias"
            }
        }
    )


class UserResponse(UserBase):
    id:int
    image_file: str | None = None
    image_path: str
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "1",
                "username": "Mat",
                "email": "mat@gmail.copm",
                "image_file": "sdsa",
                "image_path": "1asdsad.jpg",
            }
        }
    )
    pass
    

    
    
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


