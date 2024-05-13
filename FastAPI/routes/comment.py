from config.config import comments_collection
from fastapi import APIRouter
from models.comment import CommentModel
from serializers.comment import DecodeComment, DecodeComments

comment_root = APIRouter()


@comment_root.post("/blogs/{blog_id}/comments")
def create_comment(comment: CommentModel):
    comment = dict(comment)
    res = comments_collection.insert_one(comment)
    return {
        "status" : "ok"
    }

@comment_root.get("/blogs/{blog_id}/comments")
def get_comments(blog_id: str):
    comments = comments_collection.find({"blog_id": blog_id})
    decoded_data = DecodeComments(comments)
    return {
        "status" : "ok",
        "data" : decoded_data
    }