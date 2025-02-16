from pydantic import BaseModel, EmailStr, conint, Field
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class User(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode = True

class Post(PostBase):
    #id:int
    #created_at: datetime
    #user_id: int

    owner: User
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    email: EmailStr
    id: int
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)

