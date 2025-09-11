#sept 8th update
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
import uuid

from app.routers.auth import auth_router
from app.routers.books import books_router
from app.routers.admin_books import admin_books_router
from app.routers.admin_users import admin_users_router
from app.dependencies import check_database_health, users_col, get_password_hash
from app.schemas import HealthResponse

# Create default admin user on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup: Create default admin if doesn't exist
    try:
        existing_admin = await users_col.find_one({"username": "admin"})
        if not existing_admin:
            admin_user = {
                "user_id": str(uuid.uuid4()),
                "username": "admin",
                "email": "admin@bookstore.com",
                "full_name": "System Administrator",
                "password": get_password_hash("admin123"),
                "role": "admin",
                "borrowed_books": []
            }
            await users_col.insert_one(admin_user)
            print("✅ Default admin user created: admin/admin123")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"⚠️ Warning: Could not create admin user: {e}")
    
    yield
    # Shutdown: cleanup if needed
    print("📚 Book Management System shutting down...")

# Initialize FastAPI app with lifespan events
app = FastAPI(
    title="📚 Book Management System",
    description="A comprehensive book lending management system with user authentication and admin controls",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # React dev server
        "http://localhost:5000",     # Alternative frontend port
        "http://127.0.0.1:5500",     # Live Server
        "http://127.0.0.1:8080",     # Alternative dev server
        "*"  # Remove this in production and specify exact origins
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(admin_books_router)
app.include_router(admin_users_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "📚 Book Management API is running"
    }

# Health check endpoint (required by API testing)
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    db_health = await check_database_health()
    return {
        "status": db_health["status"],
        "database": db_health.get("database", "unknown"),
        "timestamp": datetime.now().isoformat()
    }

# Additional utility endpoints
@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Book Management System API",
        "version": "1.0.0",
        "description": "RESTful API for managing books and users",
        "features": [
            "User authentication & authorization",
            "Book catalog management",
            "Book borrowing/returning system", 
            "Admin user management",
            "Role-based access control"
        ]
    }