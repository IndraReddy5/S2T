from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt
from database import *
from valid_models import *
from datetime import timedelta, datetime as dt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("CRYPT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

active_keys = {}


class Token(BaseModel):
    access_token: str
    token_type: str
    exp_time: int


async def create_user(user: User):
    hashed_password = pwd_context.hash(user.password)
    check_user = await user_collection.find_one({"username": user.username})
    if check_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    await user_collection.insert_one(
        {"username": user.username, "email": user.email, "password": hashed_password}
    )


async def get_user(username: str):
    user = await user_collection.find_one({"username": username})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not pwd_context.verify(password, user.password):
        return False
    return True


async def create_token(username: str, exp_timedelta: timedelta = timedelta(minutes=10)):
    expiry_time = dt.utcnow() + exp_timedelta
    tk = Token(
        access_token=jwt.encode(
            {"username": username, "exp": expiry_time}, SECRET_KEY, algorithm=ALGORITHM
        ),
        token_type="bearer",
        exp_time=int(exp_timedelta.seconds / 60),
    )
    return tk


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        exp_time: dt = dt.utcfromtimestamp(payload.get("exp"))
        if exp_time < dt.utcnow():
            raise credentials_exception
        else:
            if username is None:
                raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_new_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        exp_time: dt = dt.utcfromtimestamp(payload.get("exp"))
        if exp_time < dt.utcnow():
            raise credentials_exception
        elif exp_time - dt.utcnow() < timedelta(minutes=5):
            return await create_token(username, timedelta(minutes=30))
        else:
            return None
    except JWTError:
        raise credentials_exception
