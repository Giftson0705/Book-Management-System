from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# --- Auth ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=80)
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

# --- Books (minimal) ---
class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]

class BookOut(BaseModel):
    id: str
    title: str
    author: str
    borrowed_by: List[str]
