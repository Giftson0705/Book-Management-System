from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import UserCreate, UserLogin
from app.middleware.auth_middleware import (
    hash_password, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.dependencies import get_database

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate, db=Depends(get_database)):
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    await db.users.insert_one({
        "username": user.username, "email": user.email, "full_name": user.full_name,
        "password": hash_password(user.password), "role": "user", "created_at": datetime.utcnow()
    })
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(credentials: UserLogin, db=Depends(get_database)):
    user = await authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user["username"], "role": user["role"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}
