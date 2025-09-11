# sept 9th

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from dependencies import users_col, oid_to_str, to_object_id
from middleware.auth_middleware import require_role
from schemas import UserOut, Message, UserRoleUpdate

admin_users_router = APIRouter(
    prefix="/api/v1/admin/users",
    tags=["Admin - Users"]
)

# -------------------------------
# Utility: normalize user
# -------------------------------
def normalize_user(user: dict) -> dict:
    norm = oid_to_str(user)
    return {
        "user_id": user.get("user_id") or norm["id"],
        "username": user.get("username"),
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "role": user.get("role", "user"),
        "borrowed_books": user.get("borrowed_books", [])
    }


# -------------------------------
# List all users
# -------------------------------
@admin_users_router.get("/", response_model=List[UserOut])
async def list_users(admin=Depends(require_role("admin"))):
    cursor = users_col.find({})
    users = []
    async for doc in cursor:
        users.append(normalize_user(doc))
    return users


# -------------------------------
# Get user by user_id (UUID or Mongo ObjectId)
# -------------------------------
@admin_users_router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, admin=Depends(require_role("admin"))):
    user = await users_col.find_one({"user_id": user_id})
    if not user:
        try:
            user = await users_col.find_one({"_id": to_object_id(user_id)})
        except Exception:
            pass

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return normalize_user(user)


# -------------------------------
# Update role (accepts JSON body { "new_role": "admin" })
# -------------------------------
@admin_users_router.put("/{user_id}", response_model=UserOut)
async def update_user_role(user_id: str, payload: UserRoleUpdate, admin=Depends(require_role("admin"))):
    # Try UUID
    result = await users_col.update_one({"user_id": user_id}, {"$set": {"role": payload.new_role}})

    if result.matched_count == 0:
        # Try Mongo ObjectId
        try:
            result = await users_col.update_one({"_id": to_object_id(user_id)}, {"$set": {"role": payload.new_role}})
        except Exception:
            pass

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch updated user
    user = await users_col.find_one({"user_id": user_id}) or \
           await users_col.find_one({"_id": to_object_id(user_id)})

    return normalize_user(user)


# -------------------------------
# Delete user
# -------------------------------
@admin_users_router.delete("/{user_id}", response_model=Message)
async def delete_user(user_id: str, admin=Depends(require_role("admin"))):
    result = await users_col.delete_one({"user_id": user_id})

    if result.deleted_count == 0:
        try:
            result = await users_col.delete_one({"_id": to_object_id(user_id)})
        except Exception:
            pass

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted successfully"}
