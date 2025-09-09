const API_BASE = "http://127.0.0.1:60619/api/v1";

async function getMe() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!res.ok) return null;
  return await res.json();
}

// Call this on page load to hydrate role safely (prevents stale role across tabs)
async function hydrateRole() {
  const me = await getMe();
  if (me) {
    localStorage.setItem("role", me.role || "user");
    localStorage.setItem("user_id", me.user_id);
    localStorage.setItem("username", me.username);
  } else {
    // token invalid
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_id");
    localStorage.removeItem("username");
    window.location.href = "login.html";
  }
}
