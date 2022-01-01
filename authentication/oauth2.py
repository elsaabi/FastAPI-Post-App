from os import sched_get_priority_max
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from validation import schema
from app_config import config

# How does an access token work? 
# After the user has provided credentials and are authenticated, server will create an access token.
# The access token gets sent back to the client. Every time the the client does an API request it will send the access token 
# to the client as part of the header request. The API will verify the token and check that it is valid. If the token is valid it 
# will process the request.
# 
# What is a JWT (JSON Web Token)? 
# It is basically just a string of characters, (that is NOT encrypted).
# 
# What is access token made up of?
# It consists of 3 pieces:
# 1. Header: includes meta data about the token (information about the token), and what algorithm and type (such as HS256 and JWT) to use
# for signing the token.
# 2. Payload: Data that you add to the payload could basically be any data (data + expireTime). Anyone will be able to see the payload so make sure 
# not to have sensitive data. A good practice is to put the userid, so that the server can see which user requested the service.
# 3. Signature: Is a combination of 3 things: Header + Payload + secret key (SECRET_KEY) (that are on the API server) and passes it into the signing
# algorithm (SHA256) hashes the information and returns a signature. This signature will be used to determine if the access token is valid. This makes
# sure that nobody has tempered our token. (Bear in mind it is not encrypted) The signature is only there for data integrity (meaning 
# making sure that no one has changed the data)

# Example of JWT Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMCIsImV4cGlyYXRpb24iOiIyMDIxLTEyLTA2IDA2OjM1OjU3LjgyOTUzMCJ9.f0U4wwyljPuJGu-qE8R8VjJDkEUhTLyvWucZIx-gRy0
# Header: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# Payload: .eyJ1c2VySWQiOiIxMCIsImV4cGlyYXRpb24iOiIyMDIxLTEyLTA2IDA2OjM1OjU3LjgyOTUzMCJ9
# Signature: .f0U4wwyljPuJGu-qE8R8VjJDkEUhTLyvWucZIx-gRy0

# to look at the data parts of a jwt access token: https://jwt.io/

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# documentation: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
# SECRET_KEY = "23449a762a0d35dfa45d4cb2e208c7aa09a2e839617d732d79bcef1f0d77c6a7" # to get a string like this from terminal: openssl rand -hex 32
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = config.settings.secret_key # to get a string like this from terminal: openssl rand -hex 32
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expires_minutes

# the data payload param can be anything that you would like the JWT to include such as userid, role type or anything else
def createAccessToken(dataPayload: dict):
    dataToEncode = dataPayload.copy()
    
    print("\ndataToEncode:")
    print(dataPayload)
    
    expireTime = str(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    print("\nexpireTime:")
    print(expireTime)
    
    dataToEncode.update({"expiration": expireTime}) 
    print("\ndataToEncode.update():")
    print(dataToEncode)
    
    # creates an access token by encoding the values: header (ALGORITHM+JWT) + payload (dataToEncode+expireTime) + secret key (SECRET_KEY) and creates a signature
    encodedJWT = jwt.encode(dataToEncode, SECRET_KEY, algorithm=ALGORITHM)
    print("\nencodedJWT:\n" + encodedJWT)
    
    return encodedJWT
    
def validateAccessToken(token: schema.TokenData = Depends(oauth2_scheme)): # identifies and forces that OAuth2PasswordBearer schema is used
    # if a Bearer token is not part of the request below exception will be raised.
    
    credentialException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"} )
    
    try:
        # decode token and extract username and expires data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userId: str = payload.get("userId")
        expires = payload.get("expiration")
        print("In oauth2.validateAccessToken() token.userId: " + str(userId))
        
        tokenData = schema.TokenData(userId=userId, expires=expires)
        
        if userId is None:
            raise credentialException
        if expires is None:
            raise credentialException
        
        if datetime.utcnow() > tokenData.expires:
            raise credentialException
    except JWTError:
        raise credentialException  
    
    return tokenData

# for test purpose
# accessToken = createAccessToken(dataPayload={"userId": "10"})
 