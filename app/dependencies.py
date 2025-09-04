# app/dependencies.py
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt

# --- Load env ---
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "book_mgmt")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# --- DB client (module-level singleton; no cyclic import risk) ---
_client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_URI)
_db = _client[MONGO_DB_NAME]

users_col = _db["users"]
books_col = _db["books"]

# --- Password hashing ---
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return _pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return _pwd_context.verify(plain_password, hashed_password)

# --- JWT helpers ---
def create_access_token(data: Dict[str, Any], expires_minutes: Optional[int] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# --- BSON/ObjectId helpers ---
def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id format")

def oid_to_str(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Utility to convert Mongo _id -> string for responses."""
    if doc and "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
