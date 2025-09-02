# routers/auth.py - Authentication routes

from datetime import timedelta, datetime
from typing import Dict
from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, Token, UserLogin
from app.middleware.auth_middleware import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.main import app

router = APIRouter()

@router.post("/signup", response_model=Dict[str, str])
async def signup(user: UserCreate):
    
    database = app.state.database
    users_collection = database.users
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = await users_collection.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "password": hashed_password,
        "role": "user",  # Default role
        "borrowed_books": [],
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_dict)
    if result.inserted_id:
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create user"
    )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):

    
    database = app.state.database
    
    user = await authenticate_user(database, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}