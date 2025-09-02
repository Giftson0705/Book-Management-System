import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

from app.routers import auth, books, admin_books, admin_users

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bookstore")

app = FastAPI(
    title="Book Management System",
    description="A complete book management system with user authentication and role-based access",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/api/v1", tags=["Books - User"])
app.include_router(admin_books.router, prefix="/api/v1/admin", tags=["Books - Admin"])
app.include_router(admin_users.router, prefix="/api/v1/admin", tags=["Users - Admin"])

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
app.state.database = database

@app.on_event("startup")
async def startup_event():
    users_collection = database.users
    books_collection = database.books
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    admin_exists = await users_collection.find_one({"role": "admin"})
    if not admin_exists:
        admin_user = {
            "username": "admin",
            "email": "admin@bookstore.com",
            "full_name": "System Administrator",
            "password": pwd_context.hash("admin123"),
            "role": "admin",
            "borrowed_books": [],
            "created_at": datetime.utcnow()
        }
        await users_collection.insert_one(admin_user)
        print("✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Please change the password after first login!")
    
    try:
        await users_collection.create_index("username", unique=True)
        await users_collection.create_index("email", unique=True)
        await books_collection.create_index("isbn", unique=True)
        await books_collection.create_index([
            ("title", "text"), 
            ("author", "text"), 
            ("genre", "text")
        ])
        print("✅ Database indexes created successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not create some indexes: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    client.close()

@app.get("/api/v1/health")
async def health_check():
    try:
        await database.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to Book Management System API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/v1/health",
            "auth": "/api/v1/auth",
            "books": "/api/v1/books",
            "admin": "/api/v1/admin"
        },
        "default_admin": {
            "username": "admin",
            "password": "admin123",
            "note": "Please change password after first login"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )