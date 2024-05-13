from fastapi import APIRouter, HTTPException
from models.blog import BlogModel, UpdateBlogModel
import datetime
from config.config import blogs_collection, user_actions_collection
from serializers.blog import DecodeBlog, DecodeBlogs
from bson import ObjectId


blog_root = APIRouter()


#new blogs
@blog_root.post('/new/blog')
def NewBlog(doc: BlogModel):
    current = datetime.date.today()
    doc = dict(doc)
    doc["date"] = str(current)

    res = blogs_collection.insert_one(doc)

    return {
        "status" : "ok",
        "message " : "Blog bloged",
        "_id" : str(res.inserted_id)
    }

#get blogs
@blog_root.get("/all/blogs")
def AllBlogs():
    res = blogs_collection.find()
    decoded_data = DecodeBlogs(res)

    return {
         "status" : "ok",
         "data" : decoded_data
    }

#get specific blog
@blog_root.get("/blog/{_id}")
def GetBlog(_id:str):
    res = blogs_collection.find_one( {"_id" : ObjectId(_id)} )

    decoded_blog = DecodeBlog(res)
    return {
        "status" : "ok",
        "data" : decoded_blog
    }

#update blog
@blog_root.patch("/update/{_id}")
def UpdateBlog(_id: str , doc: UpdateBlogModel):
    req = dict(doc)
    blogs_collection.find_one_and_update(
        {"_id" : ObjectId(_id)},
        {"$set" : req}
    )
    return {
        "status" : "ok",
        "message" : "blog updated successfully"
    }

#delete blog
@blog_root.delete("/delete/{_id}")
def DeleteBlog( _id : str ):
    blogs_collection.find_one_and_delete(
        {"_id" : ObjectId(_id)}
    )
    blogs_collection.upda
    return {
        "status" : "ok",
        "message" : "Blog deleted successfully"
    }

@blog_root.post("/blogs/{blog_id}/like")
def like_blog(blog_id: str, user_id: str):
    # Check if user already liked or disliked the blog
    existing_action = user_actions_collection.find_one({"user_id": user_id, "blog_id": blog_id})
    if existing_action:
        user_actions_collection.delete_one({"user_id": user_id, "blog_id": blog_id, "action": "like"})
        blogs_collection.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"likes": -1}})
        return {"message":"blog like removed successfully"}
    # Add user action to collection
    user_actions_collection.insert_one({"user_id": user_id, "blog_id": blog_id, "action": "like"})
    # Increment blog likes
    result = blogs_collection.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"likes": 1}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "blog liked successfully"}

@blog_root.post("/blogs/{blog_id}/dislike")
def dislike_blog(blog_id: str, user_id: str):
    # Check if user already liked or disliked the blog
    existing_action = user_actions_collection.find_one({"user_id": user_id, "blog_id": blog_id, "action":"dislike"})
    if existing_action:
        user_actions_collection.delete_one({"blog_id": blog_id, "user_id": user_id,"action":"dislike"})
        result = blogs_collection.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"dislikes": -1}})
        return {
            "message": "dislike removed successfully"
        }

    # Add user action to collection
    user_actions_collection.insert_one({"user_id": user_id, "blog_id": blog_id, "action": "dislike"})
    # Increment blog dislikes
    result = blogs_collection.update_one({"_id": ObjectId(blog_id)}, {"$inc": {"dislikes": 1}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "blog disliked successfully"}