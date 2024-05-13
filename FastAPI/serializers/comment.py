



def DecodeComment(doc) -> dict:
    return {
        "_id" : str(doc["_id"]),
        "blog_id" : str(doc["blog_id"]),
        "user_id" : str(doc["user_id"]),
        "content" : doc["content"]
        }

def DecodeComments(docs) -> list:
    return [DecodeComment(doc) for doc in docs]