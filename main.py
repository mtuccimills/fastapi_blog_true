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

from fastapi import FastAPI, Request
#from fastapi.responses import HTMLResponse # For HTML responses, not needed for API only
from fastapi.templating import Jinja2Templates # For HTML responses, not needed for API only
# To add static files
from fastapi.staticfiles import StaticFiles

# Clean Architecture modifications, adding client
from posts.client import PostClient
from posts import controller, controllerhtml

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(controller.router, prefix="/api/v1/posts", tags=["Post"])
app.include_router(controllerhtml.router, tags=["Post"])


#
#@app.get("/api/posts/{id}")
#def get_post(id: int):
#    return next((p for p in posts if p["id"] == id), None)


