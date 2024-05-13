

def DecodeBlog(doc) -> dict:
    context = {
        "_id" : str(doc["_id"]),
        "title" : doc["title"],
        "sub_title" : doc["sub_title"],
        "content" : doc["content"],
        "date" : doc["date"]
        }
    try:
        context["likes"]= doc["likes"]
    except:
        pass
    try:
        context["dislikes"]= doc["dislikes"]
    except:
        pass
    

    return context

def DecodeBlogs(docs) -> list:
    return [DecodeBlog(doc) for doc in docs]