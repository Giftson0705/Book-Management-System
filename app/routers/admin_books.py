# app/routers/admin_books.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import books_col, oid_to_str, to_object_id
from app.middleware.auth_middleware import require_role
from app.schemas import AdminBookCreate, BookUpdate, BookOut, Message

admin_books_router = APIRouter(
    prefix="/api/v1/admin/books",
    tags=["Admin - Books"]
)

# -------------------------------
# Add new book (admin only)
# -------------------------------
@admin_books_router.post("/", response_model=BookOut)
async def add_book(payload: AdminBookCreate, admin=Depends(require_role("admin"))):
    book_doc = {
        "title": payload.title,
        "author": payload.author,
        "genre": getattr(payload, "genre", None),
        "available": True
    }
    result = await books_col.insert_one(book_doc)
    book_doc["_id"] = result.inserted_id
    return oid_to_str(book_doc)

# -------------------------------
# Update book (admin only)
# -------------------------------
@admin_books_router.put("/{book_id}", response_model=BookOut)
async def update_book(book_id: str, payload: BookUpdate, admin=Depends(require_role("admin"))):
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await books_col.update_one(
        {"_id": to_object_id(book_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    book = await books_col.find_one({"_id": to_object_id(book_id)})
    return oid_to_str(book)

# -------------------------------
# Delete book (admin only)
# -------------------------------
@admin_books_router.delete("/{book_id}", response_model=Message)
async def delete_book(book_id: str, admin=Depends(require_role("admin"))):
    result = await books_col.delete_one({"_id": to_object_id(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return Message(detail="Book deleted successfully")

# -------------------------------
# List all books (admin only - monitoring)
# -------------------------------
@admin_books_router.get("/", response_model=List[BookOut])
async def list_all_books(admin=Depends(require_role("admin"))):
    cursor = books_col.find({})
    books = [oid_to_str(doc) async for doc in cursor]
    return books
