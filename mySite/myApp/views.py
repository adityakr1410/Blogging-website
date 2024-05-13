from django.shortcuts import render
import requests as Req
import json

# Create your views here.

fast_api= "http://127.0.0.1:8080/"
def home(request):

    context={
    }

    req = Req.get(fast_api+"all/blogs")
    response_dict = {
    "status_code": req.status_code,
    "headers": dict(req.headers),
    "content": req.content.decode('utf-8')  # Convert content bytes to string
}
    data = (response_dict["content"])
    data = dict(json.loads(data))
    
    data = data["data"]
    

    for x in data:
        print(x)

    context["blogs"] = data

    return render(request,'home.html',context)

def blog(request, id):

    context={}

    req = Req.get(fast_api+"blog/"+id)
    response_dict = {
    "status_code": req.status_code,
    "headers": dict(req.headers),
    "content": req.content.decode('utf-8')  # Convert content bytes to string
}
    data = (response_dict["content"])
    data = dict(json.loads(data))
    
    data = data["data"]
    context["blog"] = data

    bid=data["_id"]
    req = Req.get(fast_api+"blogs/"+bid+"/comments")
    response_dict = {
    "status_code": req.status_code,
    "headers": dict(req.headers),
    "content": req.content.decode('utf-8')  # Convert content bytes to string
}
    data = (response_dict["content"])
    data = dict(json.loads(data))
    
    data = data["data"]

    lst = []
    for x in data:
        lst.append( {
            "username": fetchUsername(x),
            "content": x["content"]
        } )
    print(lst)
    context["comments"]=lst
    context["blog_id"] = id
    context["user_id"] = "664211c72bfe1e46d09dfca8"

    return render(request, 'blog.html',context)


def fetchUsername(id):
    req = Req.get(fast_api+"userId/"+ id["user_id"])
    response_dict = {
        "status_code": req.status_code,
        "headers": dict(req.headers),
        "content": req.content.decode('utf-8')  # Convert content bytes to string
    }
    username = response_dict["content"]
    return username[1:-1]

def doLike(requset, blog, user):
    req = Req.post(fast_api+"/blogs/"+ blog +"/dislike")
    response_dict = {
    "status_code": req.status_code,
    "headers": dict(req.headers),
    "content": req.content.decode('utf-8')  # Convert content bytes to string
}
    data = (response_dict["content"])
    data = dict(json.loads(data))
    
    data = data["data"]
    

    for x in data:
        print(x)
