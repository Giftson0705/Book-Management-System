// sept 10th update

const ADMIN_USERS_API = `${API_BASE}/admin/users`;
const token = localStorage.getItem("token");

if (!token) window.lsocation.href = "login.html";

const usersList = document.getElementById("admin-users-list");

async function fetchUsers() {
  await hydrateRole(); // make sure role is fresh
  const res = await fetch(ADMIN_USERS_API, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const users = await res.json();
  renderUsers(users);
}

function renderUsers(users) {
  usersList.innerHTML = "";
  if (!users.length) {
    usersList.innerHTML = "<p>No users found.</p>";
    return;
  }

  for (const user of users) {
    const card = document.createElement("div");
    card.className = "card";
    const borrowed = (user.borrowed_books || []).length
      ? `<ul>${user.borrowed_books.map(b => `<li>${b}</li>`).join("")}</ul>`
      : "None";

    card.innerHTML = `
      <h3>${user.username}</h3>
      <p><strong>Email:</strong> ${user.email || "N/A"}</p>
      <p><strong>Role:</strong> ${user.role}</p>
      <p><strong>Borrowed Books:</strong> ${borrowed}</p>
      <button onclick="changeRole('${user.user_id}', '${user.role}')">🔑 Change Role</button>
      <button onclick="deleteUser('${user.user_id}')">🗑 Delete</button>
    `;
    usersList.appendChild(card);
  }
}

async function changeRole(userId, currentRole) {
  const newRole = currentRole === "admin" ? "user" : "admin";
  const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ new_role: newRole })
  });
  if (res.ok) {
    alert(`Role updated to ${newRole}!`);
    fetchUsers();
  } else {
    const data = await res.json().catch(() => ({}));
    alert(data.detail || "Error updating role.");
  }
}

async function deleteUser(userId) {
  if (!confirm("Are you sure you want to delete this user?")) return;
  const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` }
  });
  if (res.ok) {
    alert("User deleted!");
    fetchUsers();
  } else {
    const data = await res.json().catch(() => ({}));
    alert(data.detail || "Error deleting user.");
  }
}

document.getElementById("logout-btn")?.addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "login.html";
});

fetchUsers();

