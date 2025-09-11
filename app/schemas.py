# app/schemas.py
#sept 9th update
from typing import List, Optional, Union
from pydantic import BaseModel, Field, EmailStr

# ---------- Auth Schemas ----------
class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="user")  # "user" or "admin"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    user_id: str

# ---------- Book Schemas ----------
class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    isbn: Optional[str] = Field(None, pattern=r'^[0-9\-]{10,17}$')
    description: Optional[str] = Field(None, max_length=1000)

class BookCreate(BookBase):
    available: bool = True

class AdminBookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    isbn: Optional[str] = Field(None, pattern=r'^[0-9\-]{10,17}$')
    description: Optional[str] = Field(None, max_length=1000)
    total_copies: int = Field(default=1, ge=1, le=1000)
    available_copies: Optional[int] = Field(None, ge=0)

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = Field(None, max_length=50)
    isbn: Optional[str] = Field(None, pattern=r'^[0-9\-]{10,17}$')
    description: Optional[str] = Field(None, max_length=1000)
    total_copies: Optional[int] = Field(None, ge=1, le=1000)
    available_copies: Optional[int] = Field(None, ge=0)

class BookOut(BaseModel):
    id: str
    title: str
    author: str
    genre: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    total_copies: int = 1
    available_copies: int = 1
    available: bool = True

    class Config:
        from_attributes = True

# ---------- User Schemas ----------
class UserOut(BaseModel):
    user_id: str
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: str
    borrowed_books: List[Union[str, "BookOut"]] = []

class AdminUserOut(UserOut):
    borrowed_books: List["BookOut"] = []

class UserRoleUpdate(BaseModel):
    new_role: str = Field(pattern=r'^(user|admin)$')

# ---------- Common ----------
class Message(BaseModel):
    message: str = Field(alias="detail")
    class Config:
        populate_by_name = True

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: Optional[str] = None

UserOut.model_rebuild()
AdminUserOut.model_rebuild()
