# app/routers/admin_users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import users_col, books_col, oid_to_str, to_object_id
from app.middleware.auth_middleware import require_role
from app.schemas import AdminUserOut, Message, BookOut

admin_users_router = APIRouter(
    prefix="/api/v1/admin/users",
    tags=["Admin - Users"]
)

# -------------------------------
# Helper: hydrate borrowed_books with full BookOut
# -------------------------------
async def expand_user_books(user_doc):
    borrowed_ids = user_doc.get("borrowed_books", [])
    books = []
    if borrowed_ids:
        cursor = books_col.find({"_id": {"$in": [to_object_id(bid) for bid in borrowed_ids]}})
        books = [oid_to_str(doc) async for doc in cursor]
    user_doc["borrowed_books"] = books
    return oid_to_str(user_doc)

# -------------------------------
# List all users (admin only)
# -------------------------------
@admin_users_router.get("/", response_model=List[AdminUserOut])
async def list_users(admin=Depends(require_role("admin"))):
    cursor = users_col.find({})
    users = [await expand_user_books(doc) async for doc in cursor]
    return users

# -------------------------------
# Get user by ID (admin only)
# -------------------------------
@admin_users_router.get("/{user_id}", response_model=AdminUserOut)
async def get_user(user_id: str, admin=Depends(require_role("admin"))):
    user = await users_col.find_one({"_id": to_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await expand_user_books(user)

# -------------------------------
# Update user role (admin only)
# -------------------------------
@admin_users_router.put("/{user_id}", response_model=AdminUserOut)
async def update_user_role(user_id: str, new_role: str, admin=Depends(require_role("admin"))):
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    result = await users_col.update_one(
        {"_id": to_object_id(user_id)},
        {"$set": {"role": new_role}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    user = await users_col.find_one({"_id": to_object_id(user_id)})
    return await expand_user_books(user)

# -------------------------------
# Delete user (admin only)
# -------------------------------
@admin_users_router.delete("/{user_id}", response_model=Message)
async def delete_user(user_id: str, admin=Depends(require_role("admin"))):
    result = await users_col.delete_one({"_id": to_object_id(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return Message(detail="User deleted successfully")
