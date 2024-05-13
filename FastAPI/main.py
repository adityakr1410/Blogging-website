from fastapi import FastAPI, Request
# from routes.entry import entry_root
from routes.blog import blog_root
from routes.user import user_root
from routes.comment import comment_root
from fastapi.templating import Jinja2Templates



app = FastAPI()

# app.include_router(entry_root)
app.include_router(blog_root)
app.include_router(user_root)
app.include_router(comment_root)
