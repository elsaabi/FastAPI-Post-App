# https://fastapi.tiangolo.com/tutorial/

from typing import Set
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_config import database
from routers import user, post, auth, vote # from the folder routers import the files user, post

# from .database import SessionLocal
# The '.' (dot) means from within the same directory as this __init__.py module grab the Database class.

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

hello = 'hello world'


# try CORS:
# 1. open Chrome > ... > More tools > Developer tools
# 2. Click on Conole in menu 
# 3. fetch('http://127.0.0.1:8000/').then(res => res.json()).then(console.log)

origins = ["https://www.google.com", "https://www.youtube.com"]
# origins = [*] # allow all domains

# enable CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include our router objects
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


# HOW TO
# 1. Open VS Code
# 2. In menu File > Open Folder... > FastAPI
# 3. After project has opened. Select in menu > Terminal > New Terminal
# 4. Select virtual environment from menu > View > Command Palette... > Python: Select interpreter > Python 3.9.7 64-bit ('venv': venv)
# 5. Go to the terminal window (lower part of VSCode) > tap Terminal (right of OUTPUT)
# 6. Navigate to the app folder (in FastAPI/Api), and start the webserver.
# >> cd app
# >> uvicorn main:app --reload
# 7. Close the server by ctrl + c

    
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
# --hashing and authentication:
# pip3 install "passlib[bcrypt]"
# pip3 install "python-jose[cryptography]"
# pip3 install alembic