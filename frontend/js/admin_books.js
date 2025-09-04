const API = "http://127.0.0.1:60619/api/v1/admin/books";
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "login.html";
}

const booksList = document.getElementById("admin-books-list");
const addBookForm = document.getElementById("add-book-form");

// Fetch books
async function fetchBooks() {
  const res = await fetch(API, { headers: { Authorization: `Bearer ${token}` }});
  const books = await res.json();
  renderBooks(books);
}

// Render books
function renderBooks(books) {
  booksList.innerHTML = "";
  if (books.length === 0) {
    booksList.innerHTML = "<p class='muted'>No books found.</p>";
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
      <div class="row">
        <button class="ghost" onclick="editBook('${book.id}', '${book.title}', '${book.author}', '${book.genre || ""}')">✏️ Edit</button>
        <button class="danger" onclick="deleteBook('${book.id}')">🗑️ Delete</button>
      </div>
    `;
    booksList.appendChild(card);
  });
}

// Add book
addBookForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const genre = document.getElementById("genre").value;

  await fetch(API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, author, genre })
  });
  addBookForm.reset();
  fetchBooks();
});

// Edit book
async function editBook(id, oldTitle, oldAuthor, oldGenre) {
  const newTitle = prompt("Enter new title:", oldTitle);
  const newAuthor = prompt("Enter new author:", oldAuthor);
  const newGenre = prompt("Enter new genre:", oldGenre);

  if (!newTitle || !newAuthor) return;

  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title: newTitle, author: newAuthor, genre: newGenre })
  });
  fetchBooks();
}

// Delete book
async function deleteBook(id) {
  if (!confirm("Are you sure?")) return;
  await fetch(`${API}/${id}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  fetchBooks();
}

// Logout
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "login.html";
});

// Load books
fetchBooks();
