from passlib.context import CryptContext

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#password-hashing
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto") # defines the default hashing algorithm for passlib

# hashes the password
def hash(password: str):
    return pwdContext.hash(password)

# validates that the password provided in plain text is same as the hashed password
def verify(plainPassword, hashedPassword): 
    return pwdContext.verify(plainPassword, hashedPassword)