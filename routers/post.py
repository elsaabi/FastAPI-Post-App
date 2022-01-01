from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from fastapi.security import oauth2
import sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from app_config import database
from domain import models
from validation import schema
from authentication import oauth2

router = APIRouter(
    prefix="/posts", # the route path
    tags=['Posts']   # creates a grouping for the swagger documentation 
)

@router.get("/", response_model=List[schema.PostWithVotesResponse])
def getPosts(db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # will allow for a url like: {{URL}}/posts?limit=24&skip=0&search=welcome%20to%20funland
    print("limit: " + str(limit))
    
    # posts = db.query(models.Post).filter(models.Post.userId == payload.userId).all() # filter to get only posts for a user
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #offset is normally used for pagination
    
    posts = db.query(models.Post, func.count(models.Vote.postId).label("votes")).join( #func.count used to make a group by count
        models.Vote, models.Vote.postId == models.Post.id, isouter=True).group_by(models.Post.id).filter( #isouter ie. make it a LEFT OUTER JOIN
        models.Post.title.contains(search)).limit(limit).offset(skip).all() #offset is normally used for pagination 
    # same as SQL group by to include number of votes for a post:
    # select post.*, COUNT(vote."userId") numVotes from post LEFT OUTER JOIN vote ON post.id =  vote."postId" where post.id = 1 group by post.id order by post.id
    # Note! When joining tables with sqlalchemy as abaove the response will change therefore you will need to update the schema to match. Best way is to remove the schema and look at 
    # how it will come so that you can update the schema to match the same.

    return posts

    

# by adding userId: int = Depends(oauth2.validateAccessToken), every time post request is called we would expect a token to be passed and validated
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse) # uses the response schema class
def createPost(post: schema.PostCreate, db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):
    # fetch user data
    user = db.query(models.User).filter(models.User.id == payload.userId).first()
    print(user)  
    print(user.email) 
    print(user.password)
    
    # **post.dict() converts to format: 
    # newPost = models.Post(title=post.title, content=post.content, published=post.published)
    newPost = models.Post(userId=payload.userId, **post.dict()) # creates a new instance and initializes it through the default constructor: https://stackoverflow.com/questions/15081542/python-creating-objects
    # alternate approacth 
    # newPost.userId = payload.id # add the userId that we have stored in the payload
    db.add(newPost)
    db.commit()
    db.refresh(newPost) # retrieves the newly added record from db and stores it to newPost
    return newPost

@router.get("/{id}", response_model=schema.PostWithVotesResponse) # the "id" is called a path parameter
def getPost(id: int, db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):
    
    post = db.query(models.Post, func.count(models.Vote.postId).label("votes")).join( #func.count used to make a group by count
        models.Vote, models.Vote.postId == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first() # query without votes

    if not post:    # if we didn't find the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")
        # alternate manual way of doing above
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message:": f"post with id: {id} was not found."}
        
    # if post.userId != payload.userId: # only allow users who has created the post to view it
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform action. ")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int,  db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):
    
    postQuery = db.query(models.Post).filter(models.Post.id == id) # store the model query
    
    post = postQuery.first() # first() runs the sql query and get the result for post
    
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.userId != payload.userId: # only allow users who has created the post to delete
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform action. ")
    
    postQuery.delete(synchronize_session=False) # run query to delete post item
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.PostResponse)
def updatePost(id: int, updatedPost: schema.PostUpdate, db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):
    
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    
    post = postQuery.first() # run query to get item
    
    if post == None: # post.first() runs the sql query and get the result for post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.userId != payload.userId: # only allow users who has created the post to update
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform action. ")
    
    
    # run query again to update the item
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    # postQuery.update({'title': 'my updated title', 'content': 'this is my updated content'}, synchronize_session=False)
    
    db.commit()
    
    return postQuery.first() # run the query third time to return updated post
