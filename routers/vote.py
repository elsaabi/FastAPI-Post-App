from logging import raiseExceptions
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from fastapi.security import oauth2
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.functions import mode
from app_config import database
from domain import models
from validation import schema
from authentication import oauth2

router = APIRouter(
    prefix="/vote", # the route path
    tags=['Vote']   # creates a grouping for the swagger documentation 
)


@router.post("/", status_code=status.HTTP_201_CREATED )
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.postId).first() 
    # check if post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.postId} does not exist")
    
    # create a query that filters on both postId and userId
    existingVoteQuery = db.query(models.Vote).filter(
        models.Vote.postId == vote.postId, models.Vote.userId == payload.userId)
    
    existingVote = existingVoteQuery.first()
    
    if vote.direction == 1: # add vote
        return addVote(vote, existingVote, payload, db)
    else: # direction == 0, remove vote
        return removeVote(vote, existingVoteQuery, existingVote, payload, db)
        
def addVote(vote, existingVote, payload, db):
    # check if vote already exists
    if existingVote is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {payload.userId} has already voted on post {vote.postId}")
    
    # create a new data object model that will be saved to db
    newVote = models.Vote(postId = vote.postId, userId=payload.userId)
    db.add(newVote)
    db.commit()
    # db.refresh(newVote) # retrieves the newly added record from db and stores it to newVote
    return {"message": "Successfully added vote"}
    
    
def removeVote(vote, existingVoteQuery, existingVote, payload, db):
    # if no vote exists raise excpetion, can't delete vote if none exists
    if existingVote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
    
        # delete vote
    existingVoteQuery.delete(synchronize_session=False)
    db.commit()
    return {"message": "Successfully deleted vote"}