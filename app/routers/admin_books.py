# # routers/admin_books.py - Admin book management routes

# from typing import Dict
# from fastapi import APIRouter, HTTPException, Depends, status
# from bson import ObjectId
# from datetime import datetime
# from app.schemas import BookCreate, BookUpdate
# from app.middleware.auth_middleware import get_current_admin
# from app.main import app

# router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException, status
from app.middleware.auth_middleware import get_current_admin, book_helper
from app.dependencies import get_database
from typing import Dict, Any
from bson import ObjectId
from app.schemas import BookCreate, BookUpdate

router = APIRouter()

@router.get("/books")
async def admin_list_books(
    database=Depends(get_database),
    current_admin=Depends(get_current_admin)
):
    books_cursor = database.books.find()
    books = []
    async for book in books_cursor:
        books.append(book_helper(book))
    return books

@router.post("/books", response_model=Dict[str, str])
async def create_book(book: BookCreate, current_admin: dict = Depends(get_current_admin)):
    from app.main import app

    database = app.state.database
    books_collection = database.books
    
    # Check if book with same ISBN already exists
    existing_book = await books_collection.find_one({"isbn": book.isbn})
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )
    
    book_dict = {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "isbn": book.isbn,
        "description": book.description or "",
        "total_copies": book.total_copies,
        "available_copies": book.total_copies,
        "borrowed_by": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await books_collection.insert_one(book_dict)
    if result.inserted_id:
        return {"message": "Book created successfully", "book_id": str(result.inserted_id)}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create book"
    )

@router.put("/books/{book_id}", response_model=Dict[str, str])
async def update_book(
    book_id: str, 
    book_update: BookUpdate, 
    current_admin: dict = Depends(get_current_admin)
):
    from app.main import app

    database = app.state.database
    books_collection = database.books
    
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    
    # Check if book exists
    existing_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Prepare update data
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Handle total_copies update - adjust available_copies accordingly
    if "total_copies" in update_data:
        borrowed_count = len(existing_book.get("borrowed_by", []))
        new_total = update_data["total_copies"]
        if new_total < borrowed_count:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot set total copies to {new_total}. {borrowed_count} copies are currently borrowed."
            )
        update_data["available_copies"] = new_total - borrowed_count
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )
    
    if result.modified_count:
        return {"message": "Book updated successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to update book"
    )

@router.delete("/books/{book_id}", response_model=Dict[str, str])
async def delete_book(book_id: str, current_admin: dict = Depends(get_current_admin)):
    from app.main import app

    database = app.state.database
    books_collection = database.books
    
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    
    # Check if book exists
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if book is currently borrowed
    if book.get("borrowed_by"):
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete book that is currently borrowed"
        )
    
    result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count:
        return {"message": "Book deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete book"
    )