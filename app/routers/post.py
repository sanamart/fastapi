from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine, get_db
from typing import Optional, List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#@router.get("/posts", response_model = List[schemas.PostOut])
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # return {"message": "Hello World"}
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == current_user.id).limit(limit).offset(skip).all()

    return results

'''
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # print(f"post with id {id} was not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")
    return post
'''
#@router.get("/posts/{id}", response_model = schemas.Post)
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db),  current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    #post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # print(f"post with id {id} was not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")

    if post.Post.owner.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            , detail=f"not authorized to perform requested action")
    
    return post

'''
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    new_post = post.model_dump()
    new_post["id"] = randrange(1,10000)
    my_posts.append(new_post)
    return {"data": new_post}
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #post = post.model_dump()
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s)""", 
    #               (post.title, post.content, post.published))
    #conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    #new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

'''  
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")
    post = my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            , detail=f"not authorized to perform requested action")
    
    #post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    
    #conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

'''
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post, response: Response):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")
    post = post.model_dump()
    post["id"] = id
    my_posts[index] = post
    return post
'''    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model = schemas.Post)
def update_post(id: int, post: schemas.Post, response: Response, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, 
    #               published = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.published, id))
    #post = cursor.fetchone()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()


    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            , detail=f"post with id {id} was not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            , detail=f"not authorized to perform requested action")
    
    updated_post.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #conn.commit()
    return post