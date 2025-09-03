from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth_middleware import book_helper, get_current_user
from app.dependencies import get_database
from fastapi import Body


router = APIRouter()

@router.post("/books")
async def create_book(
    book: dict = Body(...),
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Minimal validation
    title = book.get("title")
    author = book.get("author")
    if not title or not author:
        raise HTTPException(status_code=400, detail="Title and Author are required")

    new_doc = {
        "title": title,
        "author": author,
        "borrowed_by": []
    }

    result = await db.books.insert_one(new_doc)
    created = await db.books.find_one({"_id": result.inserted_id})
    return book_helper(created)


@router.get("/books/{book_id}")
async def get_book(book_id: str, db=Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    doc = await db.books.find_one({"_id": ObjectId(book_id)})
    if not doc: raise HTTPException(status_code=404, detail="Book not found")
    return book_helper(doc)

@router.post("/books/{book_id}/borrow")
async def borrow_book(book_id: str, current_user=Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    username = current_user["username"]
    doc = await db.books.find_one({"_id": ObjectId(book_id)})
    if not doc: raise HTTPException(status_code=404, detail="Book not found")
    # allow multi-user borrowing — just add username if not present
    if username in doc.get("borrowed_by", []):
        raise HTTPException(status_code=400, detail="You already borrowed this book")
    await db.books.update_one({"_id": ObjectId(book_id)}, {"$addToSet": {"borrowed_by": username}})
    updated = await db.books.find_one({"_id": ObjectId(book_id)})
    return {"message": "Book borrowed", "book": book_helper(updated)}

@router.post("/books/{book_id}/return")
async def return_book(book_id: str, current_user=Depends(get_current_user), db=Depends(get_database)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    username = current_user["username"]
    doc = await db.books.find_one({"_id": ObjectId(book_id)})
    if not doc: raise HTTPException(status_code=404, detail="Book not found")
    if username not in doc.get("borrowed_by", []):
        raise HTTPException(status_code=400, detail="You did not borrow this book")
    await db.books.update_one({"_id": ObjectId(book_id)}, {"$pull": {"borrowed_by": username}})
    updated = await db.books.find_one({"_id": ObjectId(book_id)})
    return {"message": "Book returned", "book": book_helper(updated)}
