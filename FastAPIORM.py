# https://fastapi.tiangolo.com/tutorial/

from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
# from .database import engine, SessionLocal
from app_config import database
from domain import models
from validation import schema
from authentication import utils

# from .database import SessionLocal
# The '.' (dot) means from within the same directory as this __init__.py module grab the Database class.

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
    
@app.get("/posts", response_model=List[schema.PostResponse])
def getPosts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse) # uses the response schema class
def createPost(post: schema.PostCreate, db: Session = Depends(database.get_db)):
    # ** converts to format: 
    # newPost = models.Post(title=post.title, content=post.content, published=post.published)
    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost) # retrieves the newly added record from db and stores it to newPost
    return newPost

@app.get("/posts/{id}", response_model=schema.PostResponse) # the "id" is called a path parameter
def getPost(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:    # if we didn't find the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")
        # alternate manual way of doing above
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message:": f"post with id: {id} was not found."}
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int,  db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None: # post.first() runs the sql query and get the result for post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schema.PostResponse)
def updatePost(id: int, updatedPost: schema.PostUpdate, db: Session = Depends(database.get_db)):
    
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    
    post = postQuery.first() # run query to get item
    
    if post == None: # post.first() runs the sql query and get the result for post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    # run query again to update the item
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    # postQuery.update({'title': 'my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    
    db.commit()
    
    return postQuery.first() # run the query third time to return updated post

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse) # uses the response schema class
def createUser(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    # hash the password and save to user object
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser) # retrieves the newly added record from db and stores it to newPost
    return newUser

@app.get("/users/{id}", response_model=schema.UserResponse) # the "id" is called a path parameter
def getUser(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:    # if we didn't find the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found.")
    
    return user


# TO START SERVER:
# In the terminal type: uvicorn main:app
# Alternate to auto reload: uvicorn main:app --reload

# http methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
# http status codes:    https://www.loggly.com/blog/http-status-code-diagram/
#                       https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

# UPDATE operation: difference between put and patch. 
# When using PUT you need to send all the fields even fields that will not be updated. 
# When using PATCH you only need to send the field(s) that should be updated

# to access DOCUMENTATION
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

# create package: 
# 1. create a new folder 
# 2. create a file inside: __init__py
# 3. move your application files into the folder
# 4. when running the command from command line reference your package for example
# uvicorn app.main:app --reload (where in app.main, app is the folder/package name and main is the file of my program)

# TypeError: argument 1 must be a string or unicode object: got tuple instead:
# https://stackoverflow.com/questions/66910993/typeerror-argument-1-must-be-a-string-or-unicode-object-got-tuple-instead

# --issues when installing psycopg
# https://stormcrow.dev/en/questions/11618898?page=3

# 1. run the command: brew install postgresql
# 2. brew will be installed and updated
# 3. pip3 install psycopg2

# packages for this project:
# pip3 freeze
# pip3 install fastapi
# pip3 install pydantic
# pip3 install psycopg2
# pip3 install sqlalchemy
# pip install "passlib[bcrypt]"
    
