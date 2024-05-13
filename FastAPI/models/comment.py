from pydantic import BaseModel

class CommentModel(BaseModel):
    blog_id : str
    user_id : str
    content : str