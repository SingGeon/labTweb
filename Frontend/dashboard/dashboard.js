async function loadMe() {
  const res = await fetch("/api/me");
  const data = await res.json();

  if (!res.ok) {
    window.location.href = "/login";
    return;
  }

  const el = document.getElementById("welcomeName");
  if (el) el.textContent = `Welcome, ${data.nume}`;
}

async function logout() {
  await fetch("/api/logout", { method: "POST" });
  window.location.href = "/login";
}

document.addEventListener("DOMContentLoaded", () => {
  loadMe();
  const btn = document.getElementById("logoutBtn");
  if (btn) btn.addEventListener("click", logout);
});
