# test_api.py - API Testing Examples

import asyncio
import aiohttp
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

async def test_api():
    """Complete API testing workflow"""
    
    async with aiohttp.ClientSession() as session:
        print("🚀 Starting Book Management System API Tests\n")
        
        # 1. Test Health Check
        print("1️⃣ Testing Health Check...")
        async with session.get(f"{BASE_URL}/health") as resp:
            health = await resp.json()
            print(f"   Status: {health['status']}")
            print(f"   Database: {health['database']}\n")
        
        # 2. Register a new user
        print("2️⃣ Registering new user...")
        user_data = {
            "username": "johndoe",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "password123"
        }
        async with session.post(f"{BASE_URL}/auth/signup", json=user_data) as resp:
            if resp.status == 200:
                result = await resp.json()
                print(f"   ✅ User created: {result['message']}")
            else:
                error = await resp.json()
                print(f"   ❌ Error: {error['detail']}")
        print()
        
        # 3. Login as admin
        print("3️⃣ Logging in as admin...")
        admin_login = {
            "username": "admin",
            "password": "admin123"
        }
        async with session.post(f"{BASE_URL}/auth/login", json=admin_login) as resp:
            admin_auth = await resp.json()
            admin_token = admin_auth["access_token"]
            print(f"   ✅ Admin logged in successfully")
        print()
        
        # 4. Login as regular user
        print("4️⃣ Logging in as user...")
        user_login = {
            "username": "johndoe",
            "password": "password123"
        }
        async with session.post(f"{BASE_URL}/auth/login", json=user_login) as resp:
            user_auth = await resp.json()
            user_token = user_auth["access_token"]
            print(f"   ✅ User logged in successfully")
        print()
        
        # 5. Add books (Admin only)
        print("5️⃣ Adding books as admin...")
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        books_to_add = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Classic Literature",
                "isbn": "9780743273565",
                "description": "A classic American novel set in the Jazz Age",
                "total_copies": 5
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "genre": "Classic Literature",
                "isbn": "9780446310789",
                "description": "A gripping tale of racial injustice and childhood innocence",
                "total_copies": 3
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "genre": "Dystopian Fiction",
                "isbn": "9780451524935",
                "description": "A dystopian social science fiction novel",
                "total_copies": 4
            }
        ]
        
        book_ids = []
        for book in books_to_add:
            async with session.post(f"{BASE_URL}/admin/books", json=book, headers=admin_headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    book_ids.append(result["book_id"])
                    print(f"   ✅ Added: {book['title']}")
                else:
                    error = await resp.json()
                    print(f"   ❌ Error adding {book['title']}: {error['detail']}")
        print()
        
        # 6. Get all books (User)
        print("6️⃣ Fetching all books as user...")
        user_headers = {"Authorization": f"Bearer {user_token}"}
        async with session.get(f"{BASE_URL}/books", headers=user_headers) as resp:
            books = await resp.json()
            print(f"   ✅ Found {len(books)} books")
            for book in books:
                print(f"      📖 {book['title']} by {book['author']} ({book['available_copies']}/{book['total_copies']} available)")
        print()
        
        # 7. Search books
        print("7️⃣ Searching for 'gatsby'...")
        async with session.get(f"{BASE_URL}/books/search?query=gatsby", headers=user_headers) as resp:
            search_results = await resp.json()
            print(f"   ✅ Found {len(search_results)} matching books")
            for book in search_results:
                print(f"      📖 {book['title']}")
        print()
        
        # 8. Borrow a book
        if book_ids:
            print("8️⃣ Borrowing first book...")
            first_book_id = book_ids[0]
            async with session.post(f"{BASE_URL}/books/{first_book_id}/borrow", headers=user_headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print(f"   ✅ {result['message']}")
                else:
                    error = await resp.json()
                    print(f"   ❌ Error: {error['detail']}")
            print()
        
        # 9. View borrowed books
        print("9️⃣ Checking my borrowed books...")
        async with session.get(f"{BASE_URL}/mybooks", headers=user_headers) as resp:
            my_books = await resp.json()
            print(f"   ✅ You have {len(my_books)} borrowed books")
            for book in my_books:
                print(f"      📚 {book['title']} by {book['author']}")
        print()
        
        # 10. Get all users (Admin only)
        print("🔟 Getting all users as admin...")
        async with session.get(f"{BASE_URL}/admin/users", headers=admin_headers) as resp:
            users = await resp.json()
            print(f"   ✅ Found {len(users)} users")
            for user in users:
                print(f"      👤 {user['username']} ({user['role']}) - {len(user['borrowed_books'])} books borrowed")
        print()
        
        # 11. Return the book
        if book_ids:
            print("1️⃣1️⃣ Returning borrowed book...")
            async with session.post(f"{BASE_URL}/books/{first_book_id}/return", headers=user_headers) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    print(f"   ✅ {result['message']}")
                else:
                    error = await resp.json()
                    print(f"   ❌ Error: {error['detail']}")
            print()
        
        # 12. Test unauthorized access
        print("1️⃣2️⃣ Testing unauthorized access...")
        async with session.get(f"{BASE_URL}/books") as resp:
            if resp.status == 401:
                print("   ✅ Unauthorized access properly blocked")
            else:
                print("   ❌ Security issue: Unauthorized access allowed")
        print()
        
        # 13. Test user trying admin endpoint
        print("1️⃣3️⃣ Testing user access to admin endpoint...")
        async with session.get(f"{BASE_URL}/admin/users", headers=user_headers) as resp:
            if resp.status == 403:
                print("   ✅ Admin access properly restricted")
            else:
                print("   ❌ Security issue: User accessed admin endpoint")
        print()
        
        print("🎉 API Testing Complete!")

def run_postman_collection():
    """Generate Postman collection for API testing"""
    
    collection = {
        "info": {
            "name": "Book Management System API",
            "description": "Complete API collection for testing the Book Management System",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{access_token}}",
                    "type": "string"
                }
            ]
        },
        "event": [
            {
                "listen": "prerequest",
                "script": {
                    "type": "text/javascript",
                    "exec": [
                        ""
                    ]
                }
            }
        ],
        "variable": [
            {
                "key": "base_url",
                "value": "http://localhost:8000/api/v1",
                "type": "string"
            },
            {
                "key": "access_token",
                "value": "",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "Authentication",
                "item": [
                    {
                        "name": "Signup",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n  \"username\": \"testuser\",\n  \"email\": \"test@example.com\",\n  \"full_name\": \"Test User\",\n  \"password\": \"password123\"\n}"
                            },
                            "url": {
                                "raw": "{{base_url}}/auth/signup",
                                "host": ["{{base_url}}"],
                                "path": ["auth", "signup"]
                            }
                        }
                    },
                    {
                        "name": "Login",
                        "event": [
                            {
                                "listen": "test",
                                "script": {
                                    "exec": [
                                        "if (pm.response.code === 200) {",
                                        "    const response = pm.response.json();",
                                        "    pm.collectionVariables.set('access_token', response.access_token);",
                                        "}"
                                    ],
                                    "type": "text/javascript"
                                }
                            }
                        ],
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n  \"username\": \"admin\",\n  \"password\": \"admin123\"\n}"
                            },
                            "url": {
                                "raw": "{{base_url}}/auth/login",
                                "host": ["{{base_url}}"],
                                "path": ["auth", "login"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Books - User",
                "item": [
                    {
                        "name": "Get All Books",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/books",
                                "host": ["{{base_url}}"],
                                "path": ["books"]
                            }
                        }
                    },
                    {
                        "name": "Search Books",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/books/search?query=gatsby",
                                "host": ["{{base_url}}"],
                                "path": ["books", "search"],
                                "query": [
                                    {
                                        "key": "query",
                                        "value": "gatsby"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "name": "Get My Books",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{base_url}}/mybooks",
                                "host": ["{{base_url}}"],
                                "path": ["mybooks"]
                            }
                        }
                    }
                ]
            },
            {
                "name": "Admin - Books",
                "item": [
                    {
                        "name": "Add Book",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\n  \"title\": \"The Great Gatsby\",\n  \"author\": \"F. Scott Fitzgerald\",\n  \"genre\": \"Classic Literature\",\n  \"isbn\": \"9780743273565\",\n  \"description\": \"A classic American novel set in the Jazz Age\",\n  \"total_copies\": 5\n}"
                            },
                            "url": {
                                "raw": "{{base_url}}/admin/books",
                                "host": ["{{base_url}}"],
                                "path": ["admin", "books"]
                            }
                        }
                    }
                ]
            }
        ]
    }
    
    # Save collection to file
    with open("Book_Management_API.postman_collection.json", "w") as f:
        json.dump(collection, f, indent=2)
    
    print("📋 Postman collection saved as 'Book_Management_API.postman_collection.json'")

if __name__ == "__main__":
    print("Choose testing option:")
    print("1. Run automated API tests")
    print("2. Generate Postman collection")
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        asyncio.run(test_api())
    elif choice == "2":
        run_postman_collection()
    else:
        print("Invalid choice")