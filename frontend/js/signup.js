const API_BASE = "http://127.0.0.1:60619/api/v1";

// ---------- SIGNUP ----------
document.getElementById("signupForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Signup successful ✅ Please login.");
      window.location.href = "login.html";
    } else {
      document.getElementById("message").innerText = data.detail || "Signup failed ❌";
    }
  } catch (err) {
    document.getElementById("message").innerText = "Error connecting to server ❌";
  }
});
