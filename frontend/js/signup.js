// sept 9th update
const API_BASE = "http://127.0.0.1:60619/api/v1";

document.getElementById("signup-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const res = await fetch(`${API_BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role: "user" })
    });

    // Try to parse JSON, but guard bad gateways
    let data = null;
    try { data = await res.json(); } catch {}

    if (res.ok) {
      alert("Signup successful ✅ Please login.");
      window.location.href = "login.html";
    } else {
      document.getElementById("message").innerText =
        (data && (data.detail || data.message)) || `Signup failed (${res.status}) ❌`;
    }
  } catch (err) {
    document.getElementById("message").innerText = "Error connecting to server ❌";
  }
});

