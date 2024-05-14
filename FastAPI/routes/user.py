from fastapi import APIRouter, HTTPException,FastAPI, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta, timezone
from config.config import user_collection
from bson import ObjectId


user_root = APIRouter()

# JWT settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    username: str
    email: str
    password: str

# Register endpoint
@user_root.post("/register", response_model=User)
def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]
    user_collection.insert_one(user_data)
    return user

# Token endpoint for authentication
@user_root.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}

# Authenticate user
def authenticate_user(username: str, password: str):
    user_data = user_collection.find_one({"username": username})
    if user_data and pwd_context.verify(password, user_data["hashed_password"]):
        return user_data

# Create JWT token
def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print("Username:", username)  # Debugging print statement
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_data = user_collection.find_one({"username": username})
    print("User Data:", user_data)  # Debugging print statement
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data



# Profile endpoint
@user_root.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@user_root.get("/userId/{_id}") #made to get username for comments
def get_username(_id:str):

    res = user_collection.find_one( {"_id" : ObjectId(_id)} )

    return res["username"]

@user_root.get("/username/")
def get_userID_from_username(username:str):

    res = user_collection.find_one( {"username": username} )
    return {
        "user_ID": str(res['_id']) 
    }
