from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# field types in pydantic:
# https://pydantic-docs.helpmanual.io/usage/types/

# Schema classes that adds validation to our data model classes, that are being used for incoming requests/responses in the routers

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    createdAt: datetime
    phoneNumber: Optional[str]
    
    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel): # extends BaseModel from Pydantic package and adds validation to the incoming request params in our different CRUD methods
    title: str
    content: str
    published: bool = True # set a default value if not provided
    # rating: Optional[int] = None # makes the value fully optional, will be "none" if not provided

# extends the PostBase class by getting all available properties 'title', 'content' etc
class PostCreate(PostBase):
    pass # means that we are not adding anything to the extension

# this is just an example, in reality it wouldn't make sense to have an extension for each CRUD if they are all the same
class PostUpdate(PostBase):
    pass

class PostResponse(PostBase): # in this reponse class we are defining what properties that should be sent back as part of the response
    id: int
    createdAt: datetime
    userId: int
    # user: UserResponse # adds to return a UserResponse 
    # above you can add and remove which field you would like to have as part of the response
    
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
    class Config: # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
        orm_mode = True
        
class PostWithVotesResponse(BaseModel):
    Post: PostResponse
    votes: int
    
# By having different schema classes you can limit what the user are allowed to update. For instance:
class PostUpdateOnlySomeFields(BaseModel):
    published: bool
# This class would mean that user can only update the published property.
    
class Token(BaseModel):
    accessToken: str
    tokenType: str
    
# token data that we embedd into the access token
class TokenData(BaseModel): 
    userId: Optional[int]
    expires: Optional[datetime]
    
class Vote(BaseModel):
    postId: int
    direction: conint(le=1) # either 0 or 1: 0=remove vote, 1=add vote




