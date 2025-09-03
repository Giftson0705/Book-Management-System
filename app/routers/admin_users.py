from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_admin, user_helper
from app.dependencies import get_database

router = APIRouter()

@router.get("/users")
async def admin_list_users(db=Depends(get_database), admin=Depends(get_current_admin)):
    return [user_helper(d) async for d in db.users.find().sort("_id", -1)]

@router.delete("/users/{user_id}")
async def admin_delete_user(user_id: str, db=Depends(get_database), admin=Depends(get_current_admin)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user: raise HTTPException(status_code=404, detail="User not found")
    username = user["username"]
    # Pull username from any borrowed_by arrays across all books
    await db.books.update_many({}, {"$pull": {"borrowed_by": username}})
    res = await db.users.delete_one({"_id": ObjectId(user_id)})
    if res.deleted_count == 0: raise HTTPException(status_code=500, detail="Failed to delete user")
    return {"message": "User deleted successfully"}
