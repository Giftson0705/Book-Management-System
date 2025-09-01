# schemas.py - Pydantic schemas

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: str = Field(alias="_id")
    role: str
    borrowed_books: List[str] = []
    created_at: datetime

    class Config:
        allow_population_by_field_name = True

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1, max_length=50)
    isbn: str = Field(..., min_length=10, max_length=13)
    description: Optional[str] = Field(None, max_length=1000)
    total_copies: int = Field(..., ge=1)

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[str] = Field(None, min_length=1, max_length=50)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    description: Optional[str] = Field(None, max_length=1000)
    total_copies: Optional[int] = Field(None, ge=1)

class BookResponse(BookBase):
    id: str = Field(alias="_id")
    available_copies: int
    borrowed_by: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None