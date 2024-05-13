from pydantic import BaseModel

class BlogModel(BaseModel):
    user_id: str
    title: str
    sub_title: str
    content: str
    tags: list

class UpdateBlogModel(BaseModel):
    title: str = None
    sub_title: str = None
    content: str = None
    tags: list = None

