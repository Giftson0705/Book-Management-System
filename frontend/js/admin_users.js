// const API_BASE = "http://127.0.0.1:60619/api/v1/admin/users";
// const token = localStorage.getItem("token");

// if (!token) {
//   window.location.href = "login.html";
// }

// const usersList = document.getElementById("users-list");

// // ---------- Fetch all users ----------
// async function fetchUsers() {
//   const res = await fetch(API_BASE, {
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (!res.ok) {
//     alert("Error fetching users");
//     return;
//   }

//   const users = await res.json();
//   renderUsers(users);
// }

// // ---------- Render users ----------
// function renderUsers(users) {
//   usersList.innerHTML = "";
//   if (!users.length) {
//     usersList.innerHTML = "<p class='muted'>No users found.</p>";
//     return;
//   }

//   users.forEach(user => {
//     // If backend sends full book objects, show titles
//     const borrowed = (user.borrowed_books || [])
//       .map(b => (typeof b === "string" ? b : b.title))
//       .join(", ") || "None";

//     const card = document.createElement("div");
//     card.className = "card";
//     card.innerHTML = `
//       <h3>${user.username}</h3>
//       <p><strong>Email:</strong> ${user.email || "N/A"}</p>
//       <p><strong>Role:</strong> ${user.role}</p>
//       <p><strong>Borrowed Books:</strong> ${borrowed}</p>
//       <div class="row">
//         <button class="ghost" onclick="updateRole('${user.id}', '${user.role}')">
//           Toggle Role
//         </button>
//         <button class="danger" onclick="deleteUser('${user.id}')">Delete</button>
//       </div>
//     `;
//     usersList.appendChild(card);
//   });
// }


// // ---------- Update user role ----------
// async function updateRole(userId, currentRole) {
//   const newRole = currentRole === "admin" ? "user" : "admin";
//   if (!confirm(`Change role to ${newRole}?`)) return;

//   const res = await fetch(`${API_BASE}/${userId}?new_role=${newRole}`, {
//     method: "PUT",
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (res.ok) {
//     alert("User role updated!");
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error updating role.");
//   }
// }

// // ---------- Delete user ----------
// async function deleteUser(userId) {
//   if (!confirm("Are you sure you want to delete this user?")) return;

//   const res = await fetch(`${API_BASE}/${userId}`, {
//     method: "DELETE",
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (res.ok) {
//     alert("User deleted!");
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error deleting user.");
//   }
// }

// // ---------- Logout ----------
// document.getElementById("logout-btn").addEventListener("click", () => {
//   localStorage.removeItem("token");
//   window.location.href = "login.html";
// });

// // Load users on page load
// fetchUsers();

//////yesterday's code 
// 

////today's code

// const API_BASE = "http://127.0.0.1:60619/api/v1";
// const ADMIN_USERS_API = `${API_BASE}/admin/users`;
// const token = localStorage.getItem("token");

// if (!token) {
//   window.location.href = "login.html";
// }

// const usersList = document.getElementById("admin-users-list");

// // ---------- Fetch all users ----------
// async function fetchUsers() {
//   const res = await fetch(ADMIN_USERS_API, {
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   const users = await res.json();
//   renderUsers(users);
// }

// // ---------- Render users with admin controls ----------
// function renderUsers(users) {
//   usersList.innerHTML = "";
//   if (!users.length) {
//     usersList.innerHTML = "<p>No users found.</p>";
//     return;
//   }

//   users.forEach(user => {
//     const card = document.createElement("div");
//     card.className = "card";

//     // borrowed_books may be empty or contain ObjectId strings
//     let borrowedList = "None";
//     if (user.borrowed_books && user.borrowed_books.length > 0) {
//       borrowedList = `<ul>` + user.borrowed_books.map(id => `<li>${id}</li>`).join("") + `</ul>`;
//     }

//     card.innerHTML = `
//       <h3>${user.username}</h3>
//       <p><strong>Email:</strong> ${user.email || "N/A"}</p>
//       <p><strong>Role:</strong> ${user.role}</p>
//       <p><strong>Borrowed Books:</strong> ${borrowedList}</p>
//       <button onclick="changeRole('${user.id}', '${user.role}')">🔑 Change Role</button>
//       <button onclick="deleteUser('${user.id}')">🗑 Delete</button>
//     `;
//     usersList.appendChild(card);
//   });
// }

// // ---------- Change role ----------
// async function changeRole(userId, currentRole) {
//   const newRole = currentRole === "admin" ? "user" : "admin";

//   const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
//     method: "PUT",
//     headers: {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${token}`
//     },
//     body: JSON.stringify({ new_role: newRole })
//   });

//   if (res.ok) {
//     alert(`Role updated to ${newRole}!`);
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error updating role.");
//   }
// }

// // ---------- Delete user ----------
// async function deleteUser(userId) {
//   if (!confirm("Are you sure you want to delete this user?")) return;

//   const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
//     method: "DELETE",
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (res.ok) {
//     alert("User deleted!");
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error deleting user.");
//   }
// }

// // ---------- Logout ----------
// document.getElementById("logoutBtn").addEventListener("click", () => {
//   localStorage.removeItem("token");
//   localStorage.removeItem("role");
//   localStorage.removeItem("username");
//   window.location.href = "login.html";
// });

// // Load users on page load
// fetchUsers();


//sept 8th code
// const API_BASE = "http://127.0.0.1:60619/api/v1";
// const ADMIN_USERS_API = `${API_BASE}/admin/users`;
// const token = localStorage.getItem("token");

// if (!token) {
//   window.location.href = "login.html";
// }

// const usersList = document.getElementById("admin-users-list");

// // ---------- Fetch all users ----------
// async function fetchUsers() {
//   const res = await fetch(ADMIN_USERS_API, {
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   const users = await res.json();
//   renderUsers(users);
// }

// // ---------- Render users with admin controls ----------
// function renderUsers(users) {
//   usersList.innerHTML = "";
//   if (!users.length) {
//     usersList.innerHTML = "<p>No users found.</p>";
//     return;
//   }

//   users.forEach(user => {
//     const card = document.createElement("div");
//     card.className = "card";

//     // ✅ borrowed_books now contains full objects, not just IDs
//     let borrowedList = "None";
//     if (user.borrowed_books && user.borrowed_books.length > 0) {
//       borrowedList =
//         `<ul>` +
//         user.borrowed_books
//           .map(book => `<li>${book.title} by ${book.author}</li>`)
//           .join("") +
//         `</ul>`;
//     }

//     card.innerHTML = `
//       <h3>${user.username}</h3>
//       <p><strong>Email:</strong> ${user.email || "N/A"}</p>
//       <p><strong>Role:</strong> ${user.role}</p>
//       <p><strong>Borrowed Books:</strong> ${borrowedList}</p>
//       <button onclick="changeRole('${user.user_id}', '${user.role}')">🔑 Change Role</button>
//       <button onclick="deleteUser('${user.user_id}')">🗑 Delete</button>
//     `;
//     usersList.appendChild(card);
//   });
// }

// // ---------- Change role ----------
// async function changeRole(userId, currentRole) {
//   const newRole = currentRole === "admin" ? "user" : "admin";

//   const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
//     method: "PUT",
//     headers: {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${token}`
//     },
//     body: JSON.stringify({ new_role: newRole })
//   });

//   if (res.ok) {
//     alert(`Role updated to ${newRole}!`);
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error updating role.");
//   }
// }

// // ---------- Delete user ----------
// async function deleteUser(userId) {
//   if (!confirm("Are you sure you want to delete this user?")) return;

//   const res = await fetch(`${ADMIN_USERS_API}/${userId}`, {
//     method: "DELETE",
//     headers: { Authorization: `Bearer ${token}` }
//   });

//   if (res.ok) {
//     alert("User deleted!");
//     fetchUsers();
//   } else {
//     const data = await res.json();
//     alert(data.detail || "Error deleting user.");
//   }
// }

// // ---------- Logout ----------
// document.getElementById("logoutBtn").addEventListener("click", () => {
//   localStorage.removeItem("token");
//   localStorage.removeItem("role");
//   localStorage.removeItem("username");
//   window.location.href = "login.html";
// });

// // Load users on page load
// fetchUsers();

//sept 9th code
// const API_BASE = "http://127.0.0.1:60619/api/v1";
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

