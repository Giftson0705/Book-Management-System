# routers/admin_users.py - Admin user management routes

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from datetime import datetime
from app.middleware.auth_middleware import get_current_admin, user_helper

router = APIRouter()

@router.get("/users", response_model=List[Dict[str, Any]])
async def get_all_users(current_admin: dict = Depends(get_current_admin)):
    from main import app
    
    database = app.state.database
    users_collection = database.users
    
    users = []
    async for user in users_collection.find({}, {"password": 0}):  # Exclude password
        users.append(user_helper(user))
    return users

@router.get("/users/{user_id}", response_model=Dict[str, Any])
async def get_user_by_id(user_id: str, current_admin: dict = Depends(get_current_admin)):
    from main import app
    
    database = app.state.database
    users_collection = database.users
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await users_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_helper(user)

@router.put("/users/{user_id}", response_model=Dict[str, str])
async def update_user_role(
    user_id: str, 
    role_update: Dict[str, str], 
    current_admin: dict = Depends(get_current_admin)
):
    from main import app
    
    database = app.state.database
    users_collection = database.users
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    new_role = role_update.get("role")
    if new_role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Role must be 'user' or 'admin'")
    
    # Check if user exists
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from demoting themselves
    if str(current_admin["_id"]) == user_id and new_role != "admin":
        raise HTTPException(
            status_code=400, 
            detail="Cannot demote yourself from admin role"
        )
    
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role}}
    )
    
    if result.modified_count:
        return {"message": f"User role updated to {new_role}"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to update user role"
    )

@router.delete("/users/{user_id}", response_model=Dict[str, str])
async def delete_user(user_id: str, current_admin: dict = Depends(get_current_admin)):
    from main import app
    
    database = app.state.database
    users_collection = database.users
    books_collection = database.books
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Check if user exists
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deleting themselves
    if str(current_admin["_id"]) == user_id:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete your own account"
        )
    
    # Return all borrowed books before deleting user
    borrowed_books = user.get("borrowed_books", [])
    if borrowed_books:
        for book_id in borrowed_books:
            if ObjectId.is_valid(book_id):
                await books_collection.update_one(
                    {"_id": ObjectId(book_id)},
                    {
                        "$inc": {"available_copies": 1},
                        "$pull": {"borrowed_by": user_id},
                        "$set": {"updated_at": datetime.utcnow()}
                    }
                )
    
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return {"message": "User deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete user"
    )