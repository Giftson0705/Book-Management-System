// // frontend/js/books.js
// const API_BASE = "http://127.0.0.1:60619/api/v1";
// const token = localStorage.getItem("token");
// const role = localStorage.getItem("role");

// // Only users should be here; admins go to admin_books.html
// if (!token) window.location.replace("login.html");
// if (role === "admin") window.location.replace("admin_books.html");

// const booksList = document.getElementById("books-list");

// async function loadBooks() {
//   const res = await fetch(`${API_BASE}/books`, {
//     headers: { Authorization: `Bearer ${token}` }
//   });
//   const books = await res.json();
//   renderBooks(books);
// }

// function renderBooks(books) {
//   booksList.innerHTML = "";
//   books.forEach(book => {
//     const div = document.createElement("div");
//     div.className = "card";
//     div.innerHTML = `
//       <h3>${book.title}</h3>
//       <p><strong>Author:</strong> ${book.author}</p>
//       <p><strong>Genre:</strong> ${book.genre ?? "N/A"}</p>
//       <p><strong>Status:</strong> ${book.available ? "Available ✅" : "Borrowed ❌"}</p>
//     `;

//     if (role === "user") {
//       if (book.available) {
//         div.innerHTML += `<button onclick="borrowBook('${book.id}')">Borrow</button>`;
//       } else {
//         div.innerHTML += `<button onclick="returnBook('${book.id}')">Return</button>`;
//       }
//     }

//     booksList.appendChild(div);
//   });
// }

// async function borrowBook(id) {
//   await fetch(`${API_BASE}/books/${id}/borrow`, {
//     method: "POST",
//     headers: { Authorization: `Bearer ${token}` }
//   });
//   loadBooks();
// }

// async function returnBook(id) {
//   await fetch(`${API_BASE}/books/${id}/return`, {
//     method: "POST",
//     headers: { Authorization: `Bearer ${token}` }
//   });
//   loadBooks();
// }

// window.borrowBook = borrowBook;
// window.returnBook = returnBook;

// loadBooks();


const API = "http://127.0.0.1:60619/api/v1";
const token = localStorage.getItem("token");
if (!token) location.href = "login.html";

const booksList = document.getElementById("books-list");
const searchInput = document.getElementById("search");

let myBorrowedIds = new Set();

// Generic fetch helper
async function getJSON(url, opts = {}) {
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, ...(opts.headers || {}) },
    ...opts
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
  return res.json();
}

// Load my borrowed book IDs
async function loadMyBorrowed() {
  try {
    const mine = await getJSON(`${API}/mybooks`);
    myBorrowedIds = new Set(mine.map(b => b.id));
  } catch {
    myBorrowedIds = new Set();
  }
}

// Fetch all or search
async function fetchBooks(query = "") {
  const q = (query || "").trim();
  const url = q
    ? `${API}/books/search?query=${encodeURIComponent(q)}`
    : `${API}/books`;

  try {
    await loadMyBorrowed();
    const books = await getJSON(url);
    renderBooks(books);
  } catch (e) {
    booksList.innerHTML = `<p class="muted">Error: ${e.message}</p>`;
  }
}

// Render list
function renderBooks(books) {
  booksList.innerHTML = "";
  if (!books.length) {
    booksList.innerHTML = `<p class="muted">No books found.</p>`;
    return;
  }

  for (const book of books) {
    const card = document.createElement("div");
    card.className = "card";

    const status = book.available
      ? `<span class="badge ok">Available</span>`
      : myBorrowedIds.has(book.id)
        ? `<span class="badge busy">Borrowed (by you)</span>`
        : `<span class="badge busy">Borrowed</span>`;

    const actions = book.available
      ? `<button class="primary" onclick="borrowBook('${book.id}')">Borrow</button>`
      : myBorrowedIds.has(book.id)
        ? `<button class="ghost" onclick="returnBook('${book.id}')">Return</button>`
        : `<button class="ghost" disabled title="Borrowed by someone else">Return</button>`;

    card.innerHTML = `
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre ?? "N/A"}</p>
      <p>${status}</p>
      <div class="row">${actions}</div>
    `;
    booksList.appendChild(card);
  }
}

// Borrow
async function borrowBook(id) {
  try {
    await getJSON(`${API}/books/${id}/borrow`, { method: "POST" });
    await fetchBooks(searchInput.value);
  } catch (e) { alert(e.message); }
}

// Return
async function returnBook(id) {
  try {
    await getJSON(`${API}/books/${id}/return`, { method: "POST" });
    await fetchBooks(searchInput.value);
  } catch (e) { alert(e.message); }
}

// Debounced search
let t;
searchInput.addEventListener("input", (e) => {
  clearTimeout(t);
  t = setTimeout(() => fetchBooks(e.target.value), 280);
});

// Logout
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token");
  location.href = "login.html";
});

// Initial load
fetchBooks();
