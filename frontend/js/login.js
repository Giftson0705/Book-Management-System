//sept 9th update

const API_BASE = "http://127.0.0.1:60619/api/v1";

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);
      localStorage.setItem("username", data.username);
      localStorage.setItem("user_id", data.user_id);

      // redirect based on role
      if (data.role === "admin") {
        window.location.href = "admin_books.html";
      } else {
        window.location.href = "books.html";
      }
    } else {
      document.getElementById("message").innerText = data.detail || "Login failed ❌";
    }
  } catch (err) {
    document.getElementById("message").innerText = "Error connecting to server ❌";
  }
});
