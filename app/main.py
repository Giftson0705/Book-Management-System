import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.routers import auth, books, admin_books, admin_users

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bookstore")

app = FastAPI(title="Book Management System", version="1.1.0")

# CORS for local dev (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", "http://localhost:5500",
        "http://127.0.0.1:3000", "http://localhost:3000",
        "http://127.0.0.1", "http://localhost",
    ],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    client = AsyncIOMotorClient(MONGODB_URL)
    app.state.database = client[DATABASE_NAME]
    # Ensure the collection exists and create useful indexes
    await app.state.database.books.create_index([("title", 1)])
    await app.state.database.books.create_index([("author", 1)])
    await app.state.database.users.create_index("username", unique=True)
    await app.state.database.users.create_index("email", unique=True)

@app.on_event("shutdown")
async def shutdown():
    db = getattr(app.state, "database", None)
    if db is not None:
        db.client.close()

# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(books.router, prefix="/api/v1", tags=["books"])
app.include_router(admin_books.router, prefix="/api/v1", tags=["admin:books"])
app.include_router(admin_users.router, prefix="/api/v1/admin", tags=["admin:users"])

@app.get("/api/v1/health")
async def health():
    db_status = "ok" if getattr(app.state, "database", None) else "not-connected"
    return {"status": "healthy", "database": db_status, "ts": datetime.utcnow().isoformat() + "Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=60619, reload=True)
