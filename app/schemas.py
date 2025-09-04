# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# ---------- Auth ----------
class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="user")  # "user" or "admin"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- User ----------
class UserOut(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    role: str
    borrowed_books: List[str] = []

# ---------- Books ----------
class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    available: bool = True

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    available: Optional[bool] = None

class BookOut(BookBase):
    id: str

# ---------- Common ----------
class Message(BaseModel):
    detail: str

class AdminBookCreate(BaseModel):
    title: str
    author: str

    # ---------- Admin ----------

class AdminUserOut(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    role: str
    borrowed_books: List[BookOut] = []   # full book info instead of just IDs
