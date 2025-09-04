# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status
from app.dependencies import users_col, get_password_hash, verify_password, create_access_token, oid_to_str
from app.schemas import SignupRequest, LoginRequest, TokenResponse, UserOut
from bson import ObjectId

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=UserOut)
async def signup(payload: SignupRequest):
    existing = await users_col.find_one({"username": payload.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_doc = {
        "username": payload.username,
        "email": payload.email,
        "password": get_password_hash(payload.password),
        "role": payload.role,
        "borrowed_books": []
    }
    result = await users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return oid_to_str(user_doc)

@auth_router.post("/login")
async def login(payload: LoginRequest):
    user = await users_col.find_one({"username": payload.username})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Include role in JWT
    token = create_access_token({"id": str(user["_id"]), "role": user["role"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],       # ✅ now role is included
        "username": user["username"]
    }