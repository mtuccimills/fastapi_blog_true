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

from fastapi import FastAPI, Request, status
# To add static files
from fastapi.staticfiles import StaticFiles

# General exceptions
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException # Not used fasstapi http exception, but to better understand the exception name.

# Clean Architecture modifications, adding client
from posts import controller, controllerhtml
from directories import templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(controller.router, prefix="/api/v1/posts", tags=["Post"])
app.include_router(controllerhtml.router, tags=["Post"])

## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
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
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
