# Video 1
# Initiate the project (creates folder)
# uv init fastapi_blog_true
# Adding fastapi with STANDARD adds jinja2
# uv add "fastapi[standard]"
# Run application
# uv run fastapi dev main.py

# Video 2
# Jinja2 Templates
# Templates = dynamic data
# Past data to templates
# cicles for templates
# Standard CSS for the html
# pip install jinja2
# uv add jinja2 #This is in case you didn't used [standard] when installing fasapi

# Video 3
# exceptions
# single api response of 1 post
# Validastion errors

# Video 4
# Pydantic models and schemas
# Post endpoint to add posts

# Video 5
# Connecting to a real database with SQLAlchemy
# 3 LAYERS
# sql model
# Pydantic Schemas (accept and return from api)
# FAST API request
# pip install sqlalchemy
# uv add sqlalchemy

# Video 6
# CRUD Complete

# Video 7
# Async, use it for: I/O operation, file operation, API operation.
# FastAPI def  runs it on another loop 
# FastAPI async def runs in the main loop, ensure the await.
# pip install aiosqlite greenlet # aiosqllite asyncrononus manager for sqllite
# uv add aiosqlite greenlet
# 4:00 horas


from fastapi import FastAPI, Request, status
# To add static files
from fastapi.staticfiles import StaticFiles

# General exceptions
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException # Not used fasstapi http exception, but to better understand the exception name.

# Clean Architecture modifications, adding client
from routers.posts import controllerhtml
from routers.users import controller as controllerUser
from routers.users import controllerhtml as controllerhtmlUser
from directories import templates

# Create database
from db import Base, async_engine

#7 Async
from contextlib import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler

from routers.posts import controller
#from fastapi.responses import JSONResponse

#Syncrhonos funciton
#Base.metadata.create_all(bind=engine)
#Turned to asyncronos
@asynccontextmanager
async def lifespan(_app: FastAPI):
    #Startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await async_engine.dispose()

# Added lifespan
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")
app.include_router(controller.router, prefix="/api/v1/posts", tags=["Post"])
app.include_router(controllerhtml.router, tags=["Post"])
app.include_router(controllerUser.router, prefix="/api/v1/users", tags=["User"])
app.include_router(controllerhtmlUser.router, prefix="/users", tags=["User"])

## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
async def general_http_exception_handler(request: Request, exception: StarletteHTTPException):


    if request.url.path.startswith("/api"):
        # Async
        return await http_exception_handler(request, exception) 
        # Sync
    #     return JSONResponse(
    #         status_code=exception.status_code,
    #         content={"detail": message},
    #     )
    message = (
    exception.detail
    if exception.detail
    else "An error occurred. Please check your request and try again."
    )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        # Async
        return await request_validation_exception_handler(request, exception) 
        # Sync
        # return JSONResponse(
        #     status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        #     content={"detail": exception.errors()},
        # )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": f"Invalid request. Please check your input and try again.\n{exception.errors()}",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
