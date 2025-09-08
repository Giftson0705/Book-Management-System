// const API_BASE = "http://127.0.0.1:60619/api/v1";
// const token = localStorage.getItem("token");

// if (!token) {
//   window.location.href = "login.html";
// }

// const myBooksList = document.getElementById("mybooks-list");

// // ---------- Fetch my borrowed books ----------
// async function fetchMyBooks() {
//   const res = await fetch(`${API_BASE}/mybooks`, {
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (!res.ok) {
//     myBooksList.innerHTML = "<p>Error loading your books.</p>";
//     return;
//   }

//   const books = await res.json();
//   renderMyBooks(books);
// }

// // ---------- Render my books ----------
// function renderMyBooks(books) {
//   myBooksList.innerHTML = "";
//   if (books.length === 0) {
//     myBooksList.innerHTML = "<p>You haven’t borrowed any books yet.</p>";
//     return;
//   }

//   books.forEach(book => {
//     const card = document.createElement("div");
//     card.className = "card";
//     card.innerHTML = `
//       <h3>${book.title}</h3>
//       <p><strong>Author:</strong> ${book.author}</p>
//       <p><strong>Genre:</strong> ${book.genre || "N/A"}</p>
//       <button onclick="returnBook('${book.id}')">Return</button>
//     `;
//     myBooksList.appendChild(card);
//   });
// }

// // ---------- Return book ----------
// async function returnBook(bookId) {
//   const res = await fetch(`${API_BASE}/books/${bookId}/return`, {
//     method: "POST",
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (res.ok) {
//     alert("Book returned!");
//     fetchMyBooks();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error returning book.");
//   }
// }

// // ---------- Logout ----------
// document.getElementById("logout-btn").addEventListener("click", () => {
//   localStorage.removeItem("token");
//   window.location.href = "login.html";
// });

// // load borrowed books on page load
// fetchMyBooks();

const API_BASE = "http://127.0.0.1:60619/api/v1";
const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "login.html";
}

const myBooksList = document.getElementById("mybooks-list");

// ---------- Fetch my borrowed books ----------
async function fetchMyBooks() {
  const res = await fetch(`${API_BASE}/mybooks`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    myBooksList.innerHTML = "<p>Error loading your books.</p>";
    return;
  }

  const books = await res.json();
  renderMyBooks(books);
}

// ---------- Render my books ----------
function renderMyBooks(books) {
  myBooksList.innerHTML = "";
  if (books.length === 0) {
    myBooksList.innerHTML = "<p>You haven’t borrowed any books yet.</p>";
    return;
  }

  books.forEach(book => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${book.title}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre || "N/A"}</p>
      <button onclick="returnBook('${book.id}')">Return</button>
    `;
    myBooksList.appendChild(card);
  });
}

// ---------- Return book ----------
async function returnBook(bookId) {
  const res = await fetch(`${API_BASE}/books/${bookId}/return`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });

  if (res.ok) {
    alert("Book returned!");
    fetchMyBooks();
  } else {
    const data = await res.json();
    alert(data.detail || "Error returning book.");
  }
}

// ---------- Logout ----------
document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "login.html";
});

// load borrowed books on page load
fetchMyBooks();
