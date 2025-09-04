from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Dict, Any

from app.dependencies import decode_token, users_col, oid_to_str, to_object_id  # <-- add to_object_id
from app.schemas import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # ✅ Convert string back to ObjectId
    user = await users_col.find_one({"_id": to_object_id(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return oid_to_str(user)



def require_role(required_role: str):
    """Dependency to enforce role"""
    async def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker
