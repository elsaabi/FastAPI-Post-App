from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from starlette.status import HTTP_409_CONFLICT
from authentication import oauth2, utils
from app_config import database
from domain import models
from validation import schema

router = APIRouter(
    prefix="/users", # the route path
    tags=['Users']   # creates a grouping for the swagger documentation 
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse) # uses the response schema class
def createUser(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    
    # check if user exists
    existingUser = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existingUser is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A user with this email already exists.")
    
    # hash the password and save to user object
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    
    newUser = models.User(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser) # retrieves the newly added record from db and stores it to newPost
    return newUser

@router.get("/{id}", response_model=schema.UserResponse) # the "id" is called a path parameter
def getUser(id: int, db: Session = Depends(database.get_db), payload: schema.TokenData = Depends(oauth2.validateAccessToken)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:    # if we didn't find the post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found.")
    
    return user
