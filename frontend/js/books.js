// frontend/js/books.js
const API_BASE = "http://127.0.0.1:60619/api/v1";
const token = localStorage.getItem("token");
const role = localStorage.getItem("role");

// Only users should be here; admins go to admin_books.html
if (!token) window.location.replace("login.html");
if (role === "admin") window.location.replace("admin_books.html");

const booksList = document.getElementById("books-list");

async function loadBooks() {
  const res = await fetch(`${API_BASE}/books`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const books = await res.json();
  renderBooks(books);
}

function renderBooks(books) {
  booksList.innerHTML = "";
  books.forEach(book => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre ?? "N/A"}</p>
      <p><strong>Status:</strong> ${book.available ? "Available ✅" : "Borrowed ❌"}</p>
    `;

    if (role === "user") {
      if (book.available) {
        div.innerHTML += `<button onclick="borrowBook('${book.id}')">Borrow</button>`;
      } else {
        div.innerHTML += `<button onclick="returnBook('${book.id}')">Return</button>`;
      }
    }

    booksList.appendChild(div);
  });
}

async function borrowBook(id) {
  await fetch(`${API_BASE}/books/${id}/borrow`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  loadBooks();
}

async function returnBook(id) {
  await fetch(`${API_BASE}/books/${id}/return`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });
  loadBooks();
}

window.borrowBook = borrowBook;
window.returnBook = returnBook;

loadBooks();
