from fastapi import FastAPI, Request
from routes.entry import entry_root
from routes.blog import blog_root
from routes.user import user_root
from routes.comment import comment_root
from fastapi.templating import Jinja2Templates



app = FastAPI()

app.include_router(entry_root)
app.include_router(blog_root)
app.include_router(user_root)
app.include_router(comment_root)

templates = Jinja2Templates(directory="templates")

@app.get("/home")
def home(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.get("/register")
def registerPage(request: Request):
    

    return templates.TemplateResponse("register.html",{"request":request})

@app.post("/register")
def registerPage(request: Request):
    
    print("At last")

    return {"message": "Printed"}