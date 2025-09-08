# # app/routers/auth.py
# from fastapi import APIRouter, HTTPException, status
# from app.dependencies import users_col, get_password_hash, verify_password, create_access_token, oid_to_str
# from app.schemas import SignupRequest, LoginRequest, TokenResponse, UserOut
# from bson import ObjectId
# import uuid

# auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# @auth_router.post("/signup", response_model=UserOut)
# async def signup_user(payload: SignupRequest):
#     # Check if username exists
#     existing = await users_col.find_one({"username": payload.username})
#     if existing:
#         raise HTTPException(status_code=400, detail="Username already exists")

#     user_doc = {
#         "user_id": str(uuid.uuid4()),   # ✅ new clean ID
#         "username": payload.username,
#         "email": payload.email,
#         "password": get_password_hash(payload.password),
#         "role": payload.role or "user",
#         "borrowed_books": []
#     }

#     await users_col.insert_one(user_doc)
#     return user_doc


# # @auth_router.post("/signup", response_model=UserOut)
# # async def signup(payload: SignupRequest):
# #     existing = await users_col.find_one({"username": payload.username})
# #     if existing:
# #         raise HTTPException(status_code=400, detail="Username already exists")

# #     user_doc = {
# #         "username": payload.username,
# #         "email": payload.email,
# #         "password": get_password_hash(payload.password),
# #         "role": payload.role,
# #         "borrowed_books": []
# #     }
# #     result = await users_col.insert_one(user_doc)
# #     user_doc["_id"] = result.inserted_id
# #     return oid_to_str(user_doc)

# @auth_router.post("/login")
# async def login(payload: LoginRequest):
#     user = await users_col.find_one({"username": payload.username})
#     if not user or not verify_password(payload.password, user["password"]):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     # Include role in JWT
#     # app/routers/auth.py (inside login endpoint)

#     access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})

#     return {
#     "access_token": access_token,
#     "token_type": "bearer",
#     "role": user["role"],        # <-- return role
#     "username": user["username"]
#     }

#     # access_token = create_access_token({"id": str(user["_id"]), "role": user["role"]})

#     # return {
#     #     "access_token": token,
#     #     "token_type": "bearer",
#     #     "role": user["role"],       # ✅ now role is included
#     #     "username": user["username"]
#     # }




#sept 8th update
# app/routers/auth.py
from fastapi import APIRouter, HTTPException, status
from app.dependencies import (
    users_col,
    get_password_hash,
    verify_password,
    create_access_token,
    oid_to_str,
)
from app.schemas import SignupRequest, LoginRequest, UserOut
import uuid

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


# -------------------------------
# Signup
# -------------------------------
@auth_router.post("/signup", response_model=UserOut)
async def signup_user(payload: SignupRequest):
    # Check if username already exists
    existing = await users_col.find_one({"username": payload.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_doc = {
        "user_id": str(uuid.uuid4()),  # ✅ stable UUID
        "username": payload.username,
        "email": payload.email,
        "password": get_password_hash(payload.password),
        "role": payload.role or "user",
        "borrowed_books": [],
    }

    # Save in DB
    result = await users_col.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id  # Mongo internal _id

    # Convert _id -> id for API responses
    return oid_to_str(user_doc)


# -------------------------------
# Login
# -------------------------------
# @auth_router.post("/login")
# async def login(payload: LoginRequest):
#     user = await users_col.find_one({"username": payload.username})
#     if not user or not verify_password(payload.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#         )

#     # ✅ Use user_id in JWT (instead of username)
#     access_token = create_access_token(
#         data={"sub": user["user_id"], "role": user["role"]}
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "role": user["role"],
#         "username": user["username"],
#         "user_id": user["user_id"],  # <-- return for admin/frontend usage
#     }


# app/routers/auth.py

@auth_router.post("/login")
async def login(payload: LoginRequest):
    user = await users_col.find_one({"username": payload.username})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # ✅ Use user_id if available, else fallback to _id
    uid = user.get("user_id") or str(user["_id"])

    # Include role in JWT
    access_token = create_access_token(data={"sub": uid, "role": user["role"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user["role"],
        "username": user["username"],
        "user_id": uid   # send back for frontend clarity
    }
