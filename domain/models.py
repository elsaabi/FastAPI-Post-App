from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app_config import database

# Database schema that defines the columns of our tables within our SQL database. Used to query, create, delete and update entries withing the database.
# As soon as you create the schema class below, the corresponding table will be created in the database
class Post(database.Base):
    __tablename__ = "post"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    userId = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    
    user = relationship("User") # automatically fetches the data of of the user table as a property
    
class User(database.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phoneNumber = Column(String, nullable=True)
    
    # datatypes in Postgresql
    # https://www.postgresql.org/docs/9.5/datatype.html
    
class Vote(database.Base):
    __tablename__ = "vote"
    
    id = Column(Integer, primary_key=True, nullable=False)
    userId = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    