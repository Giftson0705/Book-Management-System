// frontend/js/session.js
(function () {
  const API_BASE = "http://127.0.0.1:60619/api/v1";

  // Clear session & redirect
  function doLogout() {
    try {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("username");
    } catch {}
    // Use replace so back button can't return to protected page
    window.location.replace("login.html");
  }

  // If a page is opened with ?logout=1, clear everything immediately
  try {
    const usp = new URLSearchParams(window.location.search);
    if (usp.get("logout") === "1") doLogout();
  } catch {}

  // Attach listener to ANY element that looks like a logout control
  document.addEventListener("click", (e) => {
    const el = e.target.closest("#logoutBtn, #logout, [data-logout]");
    if (!el) return;
    e.preventDefault();
    doLogout();
  });

  // Expose for inline onclick if needed
  window.__doLogout = doLogout;

  // Guard: if this page should be protected, redirect if there is no token
  const mustBeAuthed = document.body?.dataset?.authed === "1";
  if (mustBeAuthed) {
    const token = localStorage.getItem("token");
    if (!token) window.location.replace("login.html");
  }

  // Guard: simple role-based protection for admin pages
  const mustBeAdmin = document.body?.dataset?.admin === "1";
  if (mustBeAdmin) {
    const role = localStorage.getItem("role");
    if (role !== "admin") window.location.replace("books.html");
  }
})();
