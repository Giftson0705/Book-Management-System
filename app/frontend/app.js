const API_BASE = "http://127.0.0.1:60619/api/v1";
let token = localStorage.getItem("token") || "";

async function signup() {
  const username = document.getElementById("signup-username").value;
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  const res = await fetch(`${API_BASE}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password })
  });

  if (res.ok) {
    alert("Signup successful! Please login.");
  } else {
    alert("Signup failed.");
  }
}

async function login() {
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (res.ok) {
    const data = await res.json();
    token = data.access_token;
    localStorage.setItem("token", token);
    window.location.href = "books.html";
  } else {
    alert("Login failed.");
  }
}

async function loadBooks() {
  const res = await fetch(`${API_BASE}/books`, {
    headers: { "Authorization": "Bearer " + token }
  });

  if (res.ok) {
    const books = await res.json();
    const list = document.getElementById("books-list");
    books.forEach(book => {
      const li = document.createElement("li");
      li.textContent = `${book.title} by ${book.author}`;
      list.appendChild(li);
    });
  } else {
    alert("Failed to load books.");
  }
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}
