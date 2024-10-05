import os
from datetime import datetime, timedelta
from hashlib import md5
from ConnectionPool import r, users_collection

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt

# 生成密钥
SECRET_KEY = "your_secret_key1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HASH_SALT = "your_hash_salt"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


def hash_password(password: str):
    # using md5 + hash salt to hash password
    return md5((password + HASH_SALT).encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password

def authenticate_user(username: str, password: str):
    """Service to authenticate user

    Args:
        username (str): username
        password (str): password in plain text

    Returns:
        _type_: _description_
    """
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    if not hash_password(password) == user.get("passwordHash"):
        return False
    user.pop("passwordHash")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Service to create access token

    Args:
        data (dict): _description_
        expires_delta (Optional[timedelta], optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    to_encode = data.copy()
    r.set(data.get("sub"), 1)
    if expires_delta:
        expire = datetime.now() + expires_delta
        r.expire(data.get("sub"), int(expires_delta.total_seconds()))
    else:
        expire = datetime.now() + timedelta(minutes=15)
        r.expire(data.get("sub"), 60*15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Service to get current user, ensure the token is valid, and user is active

    Args:
        token (str, optional): required by OAuth2PasswordBearer. Defaults to Depends(oauth2_scheme).

    Raises:
        credentials_exception: HTTP_401, username is None or token is invalid
        HTTPException: HTTP_400, user is inactive

    Returns:
        _type_: _description_
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = r.get(token_data.username)
    
    if user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return token_data.username


