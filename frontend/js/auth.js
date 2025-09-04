// frontend/js/auth.js
const API_BASE = "http://127.0.0.1:60619/api/v1";

// Form might be #signup-form or #signupForm depending on page
const signupForm =
  document.getElementById("signup-form") || document.getElementById("signupForm");

const errorEl = document.getElementById("error-msg") || document.getElementById("message");

if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = (document.getElementById("username") || {}).value?.trim();
    const email = (document.getElementById("email") || {}).value?.trim() || null;
    const password = (document.getElementById("password") || {}).value?.trim();

    try {
      const res = await fetch(`${API_BASE}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password })
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        // Show detailed validation errors if provided by FastAPI
        let msg = "Signup failed";
        if (data.detail) {
          if (Array.isArray(data.detail)) {
            msg = data.detail.map(d => (d.msg || d.error || JSON.stringify(d))).join(" | ");
          } else if (typeof data.detail === "string") {
            msg = data.detail;
          }
        }
        errorEl && (errorEl.textContent = `${msg} ❌`);
        return;
      }

      alert("Signup successful! Please login.");
      window.location.replace("login.html");
    } catch (err) {
      errorEl && (errorEl.textContent = "Error connecting to server ❌");
    }
  });
}
