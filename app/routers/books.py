# # # app/routers/books.py
# # from fastapi import APIRouter, Depends, HTTPException, Query, status
# # from typing import List
# # from bson import ObjectId

# # from app.dependencies import books_col, users_col, oid_to_str, to_object_id
# # from app.middleware.auth_middleware import get_current_user
# # from app.schemas import BookOut, Message

# # books_router = APIRouter(prefix="/api/v1", tags=["Books - User"])

# # # -------------------------------
# # # List all books
# # # -------------------------------
# # @books_router.get("/books", response_model=List[BookOut])
# # async def list_books():
# #     cursor = books_col.find({})
# #     books = [oid_to_str(doc) async for doc in cursor]
# #     return books

# # # -------------------------------
# # # Get book by ID
# # # -------------------------------
# # @books_router.get("/books/{book_id}", response_model=BookOut)
# # async def get_book(book_id: str):
# #     book = await books_col.find_one({"_id": to_object_id(book_id)})
# #     if not book:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     return oid_to_str(book)

# # # -------------------------------
# # # Search books
# # # -------------------------------
# # @books_router.get("/books/search", response_model=List[BookOut])
# # async def search_books(query: str = Query(..., min_length=1)):
# #     cursor = books_col.find({
# #         "$or": [
# #             {"title": {"$regex": query, "$options": "i"}},
# #             {"author": {"$regex": query, "$options": "i"}},
# #             {"genre": {"$regex": query, "$options": "i"}},
# #         ]
# #     })
# #     books = [oid_to_str(doc) async for doc in cursor]
# #     return books

# from fastapi import APIRouter, Depends, HTTPException, Query
# from typing import List

# from app.dependencies import books_col, users_col, oid_to_str, to_object_id
# from app.middleware.auth_middleware import get_current_user
# from app.schemas import BookOut, Message

# books_router = APIRouter(prefix="/api/v1", tags=["Books - User"])


# # # -------------------------------
# # # Borrow a book (users only)
# # # -------------------------------
# @books_router.post("/books/{book_id}/borrow", response_model=Message)
# async def borrow_book(book_id: str, current_user=Depends(get_current_user)):
#     # 🚫 Prevent admins from borrowing
#     if current_user["role"] == "admin":
#         raise HTTPException(status_code=403, detail="Admins cannot borrow books")

#     book = await books_col.find_one({"_id": to_object_id(book_id)})
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     if not book.get("available", True):
#         raise HTTPException(status_code=400, detail="Book is already borrowed")

#     # Update book availability
#     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": False}})
#     # Add to user's borrowed list
#     await users_col.update_one(
#         {"_id": to_object_id(current_user["id"])},
#         {"$addToSet": {"borrowed_books": str(book["_id"])}}
#     )
#     return Message(detail="Book borrowed successfully")


# # # -------------------------------
# # # Return a book (users only)
# # # -------------------------------
# # @books_router.post("/books/{book_id}/return", response_model=Message)
# # async def return_book(book_id: str, current_user=Depends(get_current_user)):
# #     # 🚫 Prevent admins from returning
       
# #     if current_user["role"] == "admin":
# #         raise HTTPException(status_code=403, detail="Admins cannot return books")

# #     book = await books_col.find_one({"_id": to_object_id(book_id)})
# #     if not book:
# #         raise HTTPException(status_code=404, detail="Book not found")

# #     # Check if user actually borrowed it
# #     if str(book["_id"]) not in current_user.get("borrowed_books", []):
# #         raise HTTPException(status_code=400, detail="You haven’t borrowed this book")

# #     # Update book availability
# #     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": True}})
# #     # Remove from user's borrowed list
# #     await users_col.update_one(
# #         {"_id": to_object_id(current_user["id"])},
# #         {"$pull": {"borrowed_books": str(book["_id"])}}
# #     )
# #     return Message(detail="Book returned successfully")


# # # -------------------------------
# # # View my borrowed books
# # # -------------------------------
# # @books_router.get("/mybooks", response_model=List[BookOut])
# # async def my_books(current_user=Depends(get_current_user)):
# #     borrowed_ids = current_user.get("borrowed_books", [])
# #     if not borrowed_ids:
# #         return []

# #     cursor = books_col.find({"_id": {"$in": [to_object_id(bid) for bid in borrowed_ids]}})
# #     books = [oid_to_str(doc) async for doc in cursor]
# #     return books


# #sept 8th update

# # app/routers/books.py
# from fastapi import APIRouter, Depends, HTTPException, Query
# from typing import List

# from app.dependencies import books_col, users_col, oid_to_str, to_object_id
# from app.middleware.auth_middleware import get_current_user
# from app.schemas import BookOut, Message

# # books_router = APIRouter(prefix="/api/v1", tags=["Books - User"])

# # -------------------------------
# # List all books
# # -------------------------------
# @books_router.get("/books", response_model=List[BookOut])
# async def list_books():
#     cursor = books_col.find({})
#     books = [oid_to_str(doc) async for doc in cursor]
#     return books

# # -------------------------------
# # Get book by ID
# # -------------------------------
# @books_router.get("/books/{book_id}", response_model=BookOut)
# async def get_book(book_id: str):
#     book = await books_col.find_one({"_id": to_object_id(book_id)})
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return oid_to_str(book)

# # # -------------------------------
# # # Search books
# # # -------------------------------
# # # @books_router.get("/books/search", response_model=List[BookOut])
# # # async def search_books(query: str):
# # #     cursor = books_col.find({
# # #         "$or": [
# # #             {"title": {"$regex": query, "$options": "i"}},
# # #             {"author": {"$regex": query, "$options": "i"}},
# # #             {"genre": {"$regex": query, "$options": "i"}},
# # #         ]
# # #     })
# # #     books = [oid_to_str(doc) async for doc in cursor]
# # #     return books

# # @books_router.get("/search")
# # async def search_books(query: str):
# #     cursor = books_col.find({
# #         "$or": [
# #             {"title": {"$regex": query, "$options": "i"}},
# #             {"author": {"$regex": query, "$options": "i"}},
# #             {"genre": {"$regex": query, "$options": "i"}},
# #         ]
# #     })
# #     results = [oid_to_str(doc) async for doc in cursor]
# #     return results
# # all these are replaced by search feature in frontend

# # -------------------------------
# # Borrow a book (users only)
# # -------------------------------
# # @books_router.post("/books/{book_id}/borrow", response_model=Message)
# # async def borrow_book(book_id: str, current_user=Depends(get_current_user)):
# #     # 🚫 Prevent admins from borrowing
# #     if current_user["role"] == "admin":
# #         raise HTTPException(status_code=403, detail="Admins cannot borrow books")

# #     book = await books_col.find_one({"_id": to_object_id(book_id)})
# #     if not book:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     if not book.get("available", True):
# #         raise HTTPException(status_code=400, detail="Book is already borrowed")

# #     # Update book availability
# #     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": False}})

# #     # ✅ Add book to user's borrowed list using user_id
# #     await users_col.update_one(
# #         {"user_id": current_user["user_id"]},
# #         {"$addToSet": {"borrowed_books": str(book["_id"])}}
# #     )
# #     return Message(detail="Book borrowed successfully")

# # app/routers/books.py
# # @books_router.post("/{book_id}/borrow", response_model=Message)
# # async def borrow_book(book_id: str, current_user=Depends(get_current_user)):
# #     book = await books_col.find_one({"_id": to_object_id(book_id)})
# #     if not book:
# #         raise HTTPException(status_code=404, detail="Book not found")
# #     if not book.get("available", True):
# #         raise HTTPException(status_code=400, detail="Book is already borrowed")

# #     # Update book availability
# #     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": False}})

# #     # ✅ Fix: support both UUID user_id and legacy Mongo id
# #     uid = current_user.get("user_id") or current_user.get("id")

# #     await users_col.update_one(
# #         {"$or": [{"user_id": uid}, {"_id": to_object_id(uid)}]},
# #         {"$addToSet": {"borrowed_books": str(book["_id"])}}
# #     )

# #     return Message(detail="Book borrowed successfully")


# # -------------------------------
# # Return a book (users only)
# # -------------------------------
# @books_router.post("/books/{book_id}/return", response_model=Message)
# async def return_book(book_id: str, current_user=Depends(get_current_user)):
#     # 🚫 Prevent admins from returning
#     if current_user["role"] == "admin":
#         raise HTTPException(status_code=403, detail="Admins cannot return books")

#     book = await books_col.find_one({"_id": to_object_id(book_id)})
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     # Check if user actually borrowed it
#     if str(book["_id"]) not in current_user.get("borrowed_books", []):
#         raise HTTPException(status_code=400, detail="You haven’t borrowed this book")

#     # Update book availability
#     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": True}})

#     # ✅ Remove from user's borrowed list using user_id
#     await users_col.update_one(
#         {"user_id": current_user["user_id"]},
#         {"$pull": {"borrowed_books": str(book["_id"])}}
#     )
#     return Message(detail="Book returned successfully")

# # -------------------------------
# # View my borrowed books
# # -------------------------------
# @books_router.get("/mybooks", response_model=List[BookOut])
# async def my_books(current_user=Depends(get_current_user)):
#     borrowed_ids = current_user.get("borrowed_books", [])
#     if not borrowed_ids:
#         return []

#     cursor = books_col.find({"_id": {"$in": [to_object_id(bid) for bid in borrowed_ids]}})
#     books = [oid_to_str(doc) async for doc in cursor]
#     return books



# sept 10th update 2
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.dependencies import books_col, users_col, oid_to_str, to_object_id
from app.middleware.auth_middleware import get_current_user
from app.schemas import BookOut, Message

books_router = APIRouter(prefix="/api/v1", tags=["Books - User"])


# List all books
@books_router.get("/books", response_model=List[BookOut])
async def list_books():
    cursor = books_col.find({})
    books = [oid_to_str(doc) async for doc in cursor]
    return books


# Get book by ID
@books_router.get("/books/{book_id}", response_model=BookOut)
async def get_book(book_id: str):
    book = await books_col.find_one({"_id": to_object_id(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return oid_to_str(book)


# Borrow a book (users only)
@books_router.post("/books/{book_id}/borrow", response_model=Message)
async def borrow_book(book_id: str, current_user=Depends(get_current_user)):
    book = await books_col.find_one({"_id": to_object_id(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.get("available", True):
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    # Update book availability
    await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": False}})
    # Add to user's borrowed list
    await users_col.update_one(
        {"_id": to_object_id(current_user["id"])},
        {"$addToSet": {"borrowed_books": str(book["_id"])}}
    )
    return Message(detail="Book borrowed successfully")


# # Return a book (users only)
# @books_router.post("/books/{book_id}/return", response_model=Message)
# async def return_book(book_id: str, current_user=Depends(get_current_user)):
#     if current_user["role"] == "admin":
#         raise HTTPException(status_code=403, detail="Admins cannot return books")

#     book = await books_col.find_one({"_id": to_object_id(book_id)})
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     if str(book["_id"]) not in current_user.get("borrowed_books", []):
#         raise HTTPException(status_code=400, detail="You haven’t borrowed this book")

#     await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": True}})

#     await users_col.update_one(
#         {"user_id": current_user["user_id"]},
#         {"$pull": {"borrowed_books": str(book["_id"])}}
#     )
#     return Message(detail="Book returned successfully")


# # View my borrowed books
# @books_router.get("/mybooks", response_model=List[BookOut])
# async def my_books(current_user=Depends(get_current_user)):
#     borrowed_ids = current_user.get("borrowed_books", [])
#     if not borrowed_ids:
#         return []

#     cursor = books_col.find({"_id": {"$in": [to_object_id(bid) for bid in borrowed_ids]}})
#     books = [oid_to_str(doc) async for doc in cursor]
#     return books

# -------------------------------
# Return a book
# -------------------------------
@books_router.post("/books/{book_id}/return", response_model=Message)
async def return_book(book_id: str, current_user=Depends(get_current_user)):
    book = await books_col.find_one({"_id": to_object_id(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if user actually borrowed it
    if str(book["_id"]) not in current_user.get("borrowed_books", []):
        raise HTTPException(status_code=400, detail="You haven’t borrowed this book")

    # Update book availability
    await books_col.update_one({"_id": book["_id"]}, {"$set": {"available": True}})
    # Remove from user's borrowed list
    await users_col.update_one(
        {"_id": to_object_id(current_user["id"])},
        {"$pull": {"borrowed_books": str(book["_id"])}}
    )
    return Message(detail="Book returned successfully")

# -------------------------------
# View my borrowed books
# -------------------------------
@books_router.get("/mybooks", response_model=List[BookOut])
async def my_books(current_user=Depends(get_current_user)):
    borrowed_ids = current_user.get("borrowed_books", [])
    if not borrowed_ids:
        return []

    cursor = books_col.find({"_id": {"$in": [to_object_id(bid) for bid in borrowed_ids]}})
    books = [oid_to_str(doc) async for doc in cursor]
    return books