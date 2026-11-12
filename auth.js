const BASE_URL = "https://nexusbackend-production-9509.up.railway.app";

/* Toast */
function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2500);
}

/* Loader */
function showLoader() {
  document.getElementById("loader").style.display = "block";
}
function hideLoader() {
  document.getElementById("loader").style.display = "none";
}

/* LOGIN */
function login() {
  const username = document.getElementById("login_username").value;
  const password = document.getElementById("login_password").value;

  showLoader();

  fetch(BASE_URL + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        toast("Login successful");
        setTimeout(() => window.location.href = "dashboard.html", 800);
      } else {
        toast(data.detail || "Login failed");
      }
    })
    .catch(() => toast("Error logging in"))
    .finally(hideLoader);
}

/* SIGNUP */
function signup() {
  const username = document.getElementById("signup_username").value;
  const password = document.getElementById("signup_password").value;

  showLoader();

  fetch(BASE_URL + "/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      toast("Signup successful");
      setTimeout(() => window.location.href = "login.html", 800);
    })
    .catch(() => toast("Error signing up"))
    .finally(hideLoader);
}

function goTo(url) {
  document.body.classList.add("fade-out");
  setTimeout(() => window.location.href = url, 350);
}
