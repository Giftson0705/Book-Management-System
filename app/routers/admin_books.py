from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth_middleware import get_current_admin, book_helper
from app.dependencies import get_database
from app.schemas import BookCreate, BookUpdate

router = APIRouter()

@router.get("/admin/books")
async def admin_list_books(db=Depends(get_database), admin=Depends(get_current_admin)):
    return [book_helper(d) async for d in db.books.find().sort("_id", -1)]

@router.post("/books", status_code=201)
async def admin_create_book(payload: BookCreate, db=Depends(get_database), admin=Depends(get_current_admin)):
    doc = {"title": payload.title, "author": payload.author, "borrowed_by": []}
    res = await db.books.insert_one(doc)
    created = await db.books.find_one({"_id": res.inserted_id})
    return book_helper(created)

@router.put("/books/{book_id}")
async def admin_update_book(book_id: str, payload: BookUpdate, db=Depends(get_database), admin=Depends(get_current_admin)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    update = {k: v for k, v in payload.dict(exclude_unset=True).items()}
    if not update:
        doc = await db.books.find_one({"_id": ObjectId(book_id)})
        if not doc: raise HTTPException(status_code=404, detail="Book not found")
        return book_helper(doc)
    res = await db.books.update_one({"_id": ObjectId(book_id)}, {"$set": update})
    if res.matched_count == 0: raise HTTPException(status_code=404, detail="Book not found")
    updated = await db.books.find_one({"_id": ObjectId(book_id)})
    return book_helper(updated)

@router.delete("/books/{book_id}", status_code=204)
async def admin_delete_book(book_id: str, db=Depends(get_database), admin=Depends(get_current_admin)):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")
    res = await db.books.delete_one({"_id": ObjectId(book_id)})
    if res.deleted_count == 0: raise HTTPException(status_code=404, detail="Book not found")
    return {"ok": True}

