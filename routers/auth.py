from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app_config import database
from validation import schema
from domain import models
from authentication import utils, oauth2

router = APIRouter(
    tags=['Authentication'] # creates a grouping for the swagger documentation 
)

@router.post("/login", response_model=schema.Token) # response_model=schema.Token: validates that the response params of this api complies to schema.Token ie. token and tokenType
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == userCredentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    # Create a token
    accessToken = oauth2.createAccessToken(dataPayload={"userId": user.id})
    return {"accessToken": accessToken, "tokenType": "bearer"}