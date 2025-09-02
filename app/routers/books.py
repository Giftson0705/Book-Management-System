# routers/books.py - User book routes

from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query
from bson import ObjectId
from datetime import datetime
from app.middleware.auth_middleware import get_current_user, book_helper
from app.main import app

router = APIRouter()

@router.get("/books", response_model=List[Dict[str, Any]])
async def get_all_books(current_user: dict = Depends(get_current_user)):
    
    database = app.state.database
    books_collection = database.books
    
    books = []
    async for book in books_collection.find({}):
        books.append(book_helper(book))
    return books

@router.get("/books/{book_id}", response_model=Dict[str, Any])
async def get_book(book_id: str, current_user: dict = Depends(get_current_user)):
    
    database = app.state.database
    books_collection = database.books
    
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book_helper(book)

@router.get("/books/search", response_model=List[Dict[str, Any]])
async def search_books(
    query: str = Query(..., min_length=1),
    current_user: dict = Depends(get_current_user)
):
    database = app.state.database
    books_collection = database.books
    
    # Search in title, author, and genre
    search_filter = {
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"author": {"$regex": query, "$options": "i"}},
            {"genre": {"$regex": query, "$options": "i"}}
        ]
    }
    
    books = []
    async for book in books_collection.find(search_filter):
        books.append(book_helper(book))
    return books

@router.post("/books/{book_id}/borrow", response_model=Dict[str, str])
async def borrow_book(book_id: str, current_user: dict = Depends(get_current_user)):
    
    database = app.state.database
    books_collection = database.books
    users_collection = database.users
    
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    
    # Check if book exists and is available
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Check if user already borrowed this book
    user_id = str(current_user["_id"])
    if user_id in book.get("borrowed_by", []):
        raise HTTPException(status_code=400, detail="You have already borrowed this book")
    
    # Update book: decrease available copies and add user to borrowed_by
    await books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {
            "$inc": {"available_copies": -1},
            "$push": {"borrowed_by": user_id},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Update user: add book to borrowed_books
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$push": {"borrowed_books": book_id}}
    )
    
    return {"message": "Book borrowed successfully"}

@router.post("/books/{book_id}/return", response_model=Dict[str, str])
async def return_book(book_id: str, current_user: dict = Depends(get_current_user)):
    
    database = app.state.database
    books_collection = database.books
    users_collection = database.users
    
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    
    # Check if book exists
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if user has borrowed this book
    user_id = str(current_user["_id"])
    if user_id not in book.get("borrowed_by", []):
        raise HTTPException(status_code=400, detail="You haven't borrowed this book")
    
    # Update book: increase available copies and remove user from borrowed_by
    await books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {
            "$inc": {"available_copies": 1},
            "$pull": {"borrowed_by": user_id},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    # Update user: remove book from borrowed_books
    await users_collection.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"borrowed_books": book_id}}
    )
    
    return {"message": "Book returned successfully"}

@router.get("/mybooks", response_model=List[Dict[str, Any]])
async def get_my_books(current_user: dict = Depends(get_current_user)):

    
    database = app.state.database
    books_collection = database.books
    
    borrowed_book_ids = current_user.get("borrowed_books", [])
    if not borrowed_book_ids:
        return []
    
    # Convert string IDs to ObjectIds
    object_ids = [ObjectId(book_id) for book_id in borrowed_book_ids if ObjectId.is_valid(book_id)]
    
    books = []
    async for book in books_collection.find({"_id": {"$in": object_ids}}):
        books.append(book_helper(book))
    return books