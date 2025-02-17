from random import randrange
from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import SessionLocal, engine, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

'''
python -m venv .venv
source .venv/bin/activate
uvicorn app.main:app --reload
pip install 'fastapi[standard]'
pip install 'fastapi[all]'
pip install psycopg[binary] # v3
pip install psycopg2-binary # v2
pip install sqlalchemy 
pip install 'passlib[bcrypt]' 
pip install 'python-jose[cryptography]'
pip install alembic
'''

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

""" class Post(BaseModel):
    title: str
    content: str
    published: bool = True """

my_posts = [
    {
        "id": 1,
        "title": "primer viaje",
        "content": "viaje a australia"
    },
    {
        "id": 2,
        "title": "segundo viaje",
        "content": "viaje a alemania"
    }
]

try:
    # cursor_factory=RealDictCursor
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres'
                            , password='12345678', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesful")
except Exception as error:
    print("Connection to Database failed")
    print("Error: ", error)

def find_post(id):
    post = [item for item in my_posts if item["id"] == id]
    return post

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            print(i)
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
