const BASE_URL = "https://nexusbackend-production-9509.up.railway.app";

/* -------------------------------------------------
   TOAST NOTIFICATION
---------------------------------------------------*/
function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2500);
}

/* -------------------------------------------------
   LOADER
---------------------------------------------------*/
function showLoader() {
  document.getElementById("loader").style.display = "block";
}
function hideLoader() {
  document.getElementById("loader").style.display = "none";
}

/* -------------------------------------------------
   AUTH CHECK
---------------------------------------------------*/
function requireAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    toast("Please login first");
    window.location.href = "login.html";
  }
}

/* -------------------------------------------------
   LOAD USER
---------------------------------------------------*/
function loadUser() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/auth/me", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("welcome_text").textContent =
        "Welcome, " + data.username + "!";
    })
    .catch(() => toast("Failed to load user"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   PROFILE
---------------------------------------------------*/
function getProfile() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/auth/me", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("profile").innerText =
        JSON.stringify(data, null, 2);
      toast("Profile loaded");
    })
    .catch(() => toast("Error loading profile"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   FRIEND REQUESTS
---------------------------------------------------*/
function sendFriendRequest() {
  const token = localStorage.getItem("token");
  const friend = document.getElementById("friend_name").value;

  showLoader();
  fetch(BASE_URL + "/friend_requests/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ to: friend })
  })
    .then(res => res.json())
    .then(data => toast(data.message || "Request sent"))
    .catch(() => toast("Error sending request"))
    .finally(hideLoader);
}

function getFriendRequests() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/friend_requests", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("friend_requests").innerText =
        JSON.stringify(data, null, 2);
      toast("Friend requests loaded");
    })
    .catch(() => toast("Error loading friend requests"))
    .finally(hideLoader);
}

function getFriends() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/friends", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("friends").innerText =
        JSON.stringify(data, null, 2);
      toast("Friends loaded");
    })
    .catch(() => toast("Error loading friends"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   CHAT
---------------------------------------------------*/
function sendChat() {
  const token = localStorage.getItem("token");
  const to = document.getElementById("chat_to").value;
  const msg = document.getElementById("chat_msg").value;

  showLoader();
  fetch(BASE_URL + "/chat/send", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ to, message: msg })
  })
    .then(res => res.json())
    .then(data => toast(data.message || "Message sent"))
    .catch(() => toast("Error sending message"))
    .finally(hideLoader);
}

function getChat() {
  const token = localStorage.getItem("token");
  const to = document.getElementById("chat_to").value;

  showLoader();
  fetch(BASE_URL + "/chat/history/" + to, {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("chat").innerText =
        JSON.stringify(data, null, 2);
      toast("Chat loaded");
    })
    .catch(() => toast("Error loading chat"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   NOTIFICATIONS
---------------------------------------------------*/
function getNotifications() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/notifications", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("notifications").innerText =
        JSON.stringify(data, null, 2);
      toast("Notifications loaded");
    })
    .catch(() => toast("Error loading notifications"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   TOURNAMENTS
---------------------------------------------------*/
function getTournaments() {
  showLoader();
  fetch(BASE_URL + "/tournaments")
    .then(res => res.json())
    .then(data => {
      document.getElementById("tournaments").innerText =
        JSON.stringify(data, null, 2);
      toast("Tournaments loaded");
    })
    .catch(() => toast("Error loading tournaments"))
    .finally(hideLoader);
}

function joinTournament() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/tournaments/join", {
    method: "POST",
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => toast(data.message || "Joined tournament"))
    .catch(() => toast("Error joining tournament"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   LEADERBOARD
---------------------------------------------------*/
function getLeaderboard() {
  showLoader();
  fetch(BASE_URL + "/leaderboard/top")
    .then(res => res.json())
    .then(data => {
      const div = document.getElementById("leaderboard");
      div.innerHTML = "";
      const list = data.top || data;

      list.forEach(p => {
        const el = document.createElement("div");
        el.className = "leader-card";

        const nameSpan = document.createElement("span");
        nameSpan.textContent = p.username || "Unknown";

        const scoreSpan = document.createElement("span");
        scoreSpan.className = "score";
        scoreSpan.textContent = p.score ?? 0;

        el.appendChild(nameSpan);
        el.appendChild(scoreSpan);
        div.appendChild(el);
      });

      toast("Leaderboard loaded");
    })
    .catch(() => toast("Error loading leaderboard"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   MATCHES
---------------------------------------------------*/
function addMatch() {
  const token = localStorage.getItem("token");
  const score = document.getElementById("match_score").value;
  const result = document.getElementById("match_result").value;

  showLoader();
  fetch(BASE_URL + "/match/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({ score, result })
  })
    .then(res => res.json())
    .then(data => toast(data.message || "Match added"))
    .catch(() => toast("Error adding match"))
    .finally(hideLoader);
}

function getMatches() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/match/my", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("matches").innerText =
        JSON.stringify(data, null, 2);
      toast("Match history loaded");
    })
    .catch(() => toast("Error loading matches"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   BADGES
---------------------------------------------------*/
function getBadges() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/badges", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("badges").innerText =
        JSON.stringify(data, null, 2);
      toast("Badges loaded");
    })
    .catch(() => toast("Error loading badges"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   ACTIVITY
---------------------------------------------------*/
function getActivity() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/activity", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("activity").innerText =
        JSON.stringify(data, null, 2);
      toast("Activity loaded");
    })
    .catch(() => toast("Error loading activity"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   SEARCH
---------------------------------------------------*/
function searchUser() {
  const name = document.getElementById("search_user").value;

  showLoader();
  fetch(BASE_URL + "/search/" + name)
    .then(res => res.json())
    .then(data => {
      document.getElementById("search").innerText =
        JSON.stringify(data, null, 2);
      toast("Search complete");
    })
    .catch(() => toast("Error searching user"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   BLOCK
---------------------------------------------------*/
function blockUser() {
  const token = localStorage.getItem("token");
  const user = document.getElementById("block_user").value;

  showLoader();
  fetch(BASE_URL + "/block/" + user, {
    method: "POST",
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => toast(data.message || "User blocked"))
    .catch(() => toast("Error blocking user"))
    .finally(hideLoader);
}

function getBlocked() {
  const token = localStorage.getItem("token");

  showLoader();
  fetch(BASE_URL + "/block", {
    headers: { "Authorization": "Bearer " + token }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("blocked").innerText =
        JSON.stringify(data, null, 2);
      toast("Blocked users loaded");
    })
    .catch(() => toast("Error loading blocked users"))
    .finally(hideLoader);
}

/* -------------------------------------------------
   DARK MODE
---------------------------------------------------*/
function toggleDarkMode() {
  document.body.classList.toggle("dark");
  toast("Theme updated");
}

/* -------------------------------------------------
   LOGOUT
---------------------------------------------------*/
function logout() {
  localStorage.removeItem("token");
  toast("Logged out");
  setTimeout(() => window.location.href = "login.html", 800);
}

/* -------------------------------------------------
   INIT
---------------------------------------------------*/
document.addEventListener("DOMContentLoaded", () => {
  requireAuth();
  loadUser();
});

function scrollToBox(id) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    toast(id.charAt(0).toUpperCase() + id.slice(1) + " section opened");
  }
}
