# app/main.py
from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.books import books_router
from app.routers.admin_books import admin_books_router
from app.routers.admin_users import admin_users_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="📚 Book Management System")

# Allow frontend or Postman to access your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(admin_books_router)
app.include_router(admin_users_router)

@app.get("/")
async def root():
    return {"message": "Book Management API running"}
