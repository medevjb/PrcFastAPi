from mimetypes import init
import os

from fastapi import FastAPI, Depends, HTTPException, Header
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from config import config

# import os
# from dotenv import load_dotenv

app = FastAPI()
# load_dotenv()

#Jwt Configuration
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.ACCESS_TOKEN_EXPIRE_MINUTES)

#Password Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Oatuth Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Fake dummy user database for demonstration purposes
fake_users_db = {
    "user": {
        "username": "user",
        "hashed_password": pwd_context.hash("password")
    }
}

# Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#hash Passowrd
def hash_password(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)


    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


@app.post("/login")
def login(from_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(from_data.username)

    if not user or not verify_password(from_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

    

def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"sub": username}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



#protected Route
@app.get("/protected")
def protected_route(username:str = Depends(verify_token)):
    return {
        "message": f"Hello, {username}! This is a protected route."
    }

    