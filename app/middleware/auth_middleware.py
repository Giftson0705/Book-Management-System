#sept 9th update
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Dict, Any

from app.dependencies import decode_token, users_col, to_object_id, oid_to_str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = decode_token(token)
        uid: str = payload.get("sub")
        if uid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing user ID")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Try by user_id (new schema)
    user = await users_col.find_one({"user_id": uid})
    if not user:
        # Fallback: treat as legacy ObjectId
        try:
            user = await users_col.find_one({"_id": to_object_id(uid)})
        except Exception:
            user = None

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Normalize _id => id, keep user_id if present
    return oid_to_str(user)

def require_role(required_role: str):
    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

require_admin = require_role("admin")
require_user = require_role("user")
