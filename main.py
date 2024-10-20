
from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List, Dict, Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from models import Base, User, Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser, PostCreate, PostResponce



app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()


@app.post("/users/add", response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/posts/add", response_model=PostResponce)
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponce:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get("/posts", response_model=List[PostResponce])
async def get_all_posts(db: Session = Depends(get_db)) -> List[PostResponce]:
    return db.query(Post).all()

@app.get("/users", response_model=List[DbUser])
async def get_all_user(db: Session = Depends(get_db)) -> List[DbUser]:
    return db.query(User).all()

@app.get("/posts/{id}", response_model=PostResponce)
async def get_user(id: int, db: Session = Depends(get_db)) -> PostResponce:
    return db.query(Post).filter(Post.id == id).first()

@app.get("/users/{id}", response_model=DbUser)
async def get_user(id: int, db: Session = Depends(get_db)) -> DbUser:
    return db.query(User).filter(User.id == id).first()

