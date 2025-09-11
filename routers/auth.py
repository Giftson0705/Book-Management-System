#sept 9th update 
from fastapi import APIRouter, HTTPException, status, Depends
from dependencies import (
    users_col, get_password_hash, verify_password, create_access_token,
    oid_to_str
)
from schemas import SignupRequest, LoginRequest, UserOut, TokenResponse
from middleware.auth_middleware import get_current_user
import uuid

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=UserOut)
async def signup_user(payload: SignupRequest):
    existing = await users_col.find_one({"username": payload.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_doc = {
        "user_id": str(uuid.uuid4()),
        "username": payload.username,
        "email": payload.email,
        "full_name": payload.full_name,
        "password": get_password_hash(payload.password),
        "role": payload.role or "user",
        "borrowed_books": []
    }
    await users_col.insert_one(user_doc)
    # ensure consistent shape
    return {
        "user_id": user_doc["user_id"],
        "username": user_doc["username"],
        "email": user_doc.get("email"),
        "full_name": user_doc.get("full_name"),
        "role": user_doc.get("role", "user"),
        "borrowed_books": []
    }

@auth_router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await users_col.find_one({"username": payload.username})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    uid = user.get("user_id") if isinstance(user.get("user_id"), str) else oid_to_str(user).get("id")
    role = user.get("role", "user")

    access_token = create_access_token(data={"sub": uid, "role": role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role,
        "username": user["username"],
        "user_id": uid
    }

@auth_router.get("/me", response_model=UserOut)
async def who_am_i(current_user = Depends(get_current_user)):
    """
    Return fresh user info from token. Frontend should call this on page load
    instead of trusting localStorage role blindly.
    """
    # current_user already normalized by oid_to_str in middleware
    # ensure user_id is present
    uid = current_user.get("user_id") or current_user.get("id")
    return {
        "user_id": uid,
        "username": current_user["username"],
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name"),
        "role": current_user.get("role", "user"),
        "borrowed_books": current_user.get("borrowed_books", [])
    }
