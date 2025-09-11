//sept 10th update

const API_BASE = "http://127.0.0.1:60619/api/v1/admin";
const ADMIN_BOOKS_API = `${API_BASE}/books`;
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "login.html";
}

const booksList = document.getElementById("admin-books-list");
const addBookForm = document.getElementById("add-book-form");

// ---------- Fetch all books ----------
async function fetchBooks() {
  const res = await fetch(`${API_BASE}/books`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  const books = await res.json();
  renderBooks(books);
}

// ---------- Render books with admin controls ----------
function renderBooks(books) {
  booksList.innerHTML = "";
  if (!books.length) {
    booksList.innerHTML = "<p>No books found.</p>";
    return;
  }

  books.forEach(book => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre || "N/A"}</p>
      <p><strong>Status:</strong> ${book.available ? "Available ✅" : "Borrowed ❌"}</p>
      <button onclick="deleteBook('${book.id}')">🗑 Delete</button>
      <button onclick="editBook('${book.id}', '${book.title}', '${book.author}', '${book.genre || ""}')">✏️ Edit</button>
    `;
    booksList.appendChild(card);
  });
}

// ---------- Add new book ----------
addBookForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const genre = document.getElementById("genre").value;

  const res = await fetch(ADMIN_BOOKS_API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, author, genre })
  });

  if (res.ok) {
    alert("Book added!");
    addBookForm.reset();
    fetchBooks();
  } else {
    const data = await res.json();
    alert(data.detail || "Error adding book.");
  }
});

// ---------- Delete book ----------
async function deleteBook(bookId) {
  if (!confirm("Are you sure you want to delete this book?")) return;

  const res = await fetch(`${ADMIN_BOOKS_API}/${bookId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });

  if (res.ok) {
    alert("Book deleted!");
    fetchBooks();
  } else {
    const data = await res.json();
    alert(data.detail || "Error deleting book.");
  }
}

// ---------- Edit book ----------
async function editBook(bookId, title, author, genre) {
  const newTitle = prompt("Enter new title:", title);
  const newAuthor = prompt("Enter new author:", author);
  const newGenre = prompt("Enter new genre:", genre);

  if (!newTitle || !newAuthor) return;

  const res = await fetch(`${ADMIN_BOOKS_API}/${bookId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title: newTitle, author: newAuthor, genre: newGenre })
  });

  if (res.ok) {
    alert("Book updated!");
    fetchBooks();
  } else {
    const data = await res.json();
    alert(data.detail || "Error updating book.");
  }
}

// ---------- Logout ----------
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  window.location.href = "login.html";
});

// Load books on page load
fetchBooks();



