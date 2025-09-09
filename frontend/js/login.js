// // frontend/js/login.js
// const API_BASE = "http://127.0.0.1:60619/api/v1";

// // If already logged in, bounce to the right place
// (function () {
//   const token = localStorage.getItem("token");
//   const role = localStorage.getItem("role");
//   if (token && role) {
//     window.location.replace(role === "admin" ? "admin_books.html" : "books.html");
//   }
// })();

// const form = document.getElementById("loginForm") || document.getElementById("login-form");
// const messageEl = document.getElementById("message") || document.getElementById("error-msg");

// if (form) {
//   form.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     const username = (document.getElementById("username") || {}).value?.trim();
//     const password = (document.getElementById("password") || {}).value?.trim();

//     try {
//       const res = await fetch(`${API_BASE}/auth/login`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ username, password })
//       });

//       const data = await res.json().catch(() => ({}));

//       if (!res.ok) {
//         const msg = data.detail || "Login failed";
//         messageEl && (messageEl.textContent = `${msg} ❌`);
//         return;
//       }

//       localStorage.setItem("token", data.access_token);
//       localStorage.setItem("role", data.role);
//       localStorage.setItem("username", data.username);

//       messageEl && (messageEl.textContent = "Login successful ✅");

//       setTimeout(() => {
//         window.location.replace(data.role === "admin" ? "admin_books.html" : "books.html");
//       }, 600);
//     } catch (err) {
//       messageEl && (messageEl.textContent = "Error connecting to server ❌");
//     }
//   });
// }

//sept 9th update

const API_BASE = "http://127.0.0.1:60619/api/v1";

document.getElementById("loginForm").addEventListener("submit", async (e) => {
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
