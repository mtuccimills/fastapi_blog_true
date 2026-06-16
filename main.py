# Comments
# Initiate the project (creates folder)
# uv init fastapi_blog_true
# Adding fastapi with STANDARD
# uv add "fastapi[standard]"
# Run application
# uv run fastapi dev main.py

from fastapi import FastAPI
from fastapi.responses import HTMLResponse # For HTML responses, not needed for API only

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

@app.get("/"
         , response_class=HTMLResponse # For HTML responses, not needed for API only
         , include_in_schema= False
         )
@app.get("/posts"
         , response_class=HTMLResponse # For HTML responses, not needed for API only
         , include_in_schema= False
         )
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/api/posts")
def get_posts():
    return posts
