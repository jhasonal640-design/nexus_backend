const BASE_URL = "http://127.0.0.1:8000";

/* REGISTER */
function signup() {
  console.log("Signup function running...");
  const username = document.getElementById("su_user").value;
  const password = document.getElementById("su_pass").value;
  // Use BASE_URL so the endpoint can be changed in one place
  fetch(BASE_URL + "/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      console.log("Response:", data);
      alert("Signup successful!");
    })
    .catch(err => {
      console.error("Error:", err);
      alert("Signup failed");
    });
}


/* LOGIN */
function login() {
  const username = document.getElementById("li_user").value;
  const password = document.getElementById("li_pass").value;

  if (!username || !password) {
    alert("Please enter username and password");
    return;
  }

  fetch(BASE_URL + "/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.token) {
        localStorage.setItem("token", data.token);
        alert("Login successful");
        window.location.href = "dashboard.html";
      } else {
        alert("Login failed");
      }
    })
    .catch(err => {
      console.error(err);
      alert("Login error");
    });
}


/* GET PROFILE */
function getProfile() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login first");
    return;
  }

  fetch(BASE_URL + "/profile/me", {
    headers: {
      "Authorization": "Bearer " + token
    }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("profile").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
      console.error(err);
      alert("Error loading profile");
    });
}

/* LEADERBOARD TOP */
function getLeaderboard() {
  fetch(BASE_URL + "/leaderboard/top")
    .then(res => res.json())
    .then(data => {
      const leaderboardDiv = document.getElementById("leaderboard");
      leaderboardDiv.innerHTML = "";

      data.forEach(player => {
        const card = document.createElement("div");
        card.className = "leader-card";
        card.innerText = `${player.username} — ${player.score}`;
        leaderboardDiv.appendChild(card);
      });
    })
    .catch(err => {
      console.error(err);
      alert("Error loading leaderboard");
    });
}

/* ADD MATCH */
function addMatch() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login first");
    return;
  }

  const score = document.getElementById("match_score").value;
  const result = document.getElementById("match_result").value;

  if (!score || !result) {
    alert("Please enter score and result");
    return;
  }

  fetch(BASE_URL + "/match/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    },
    body: JSON.stringify({
      score: Number(score),
      result: result
    })
  })
    .then(res => res.json())
    .then(data => {
      alert("Match added!");
      console.log(data);
    })
    .catch(err => {
      console.error(err);
      alert("Error adding match");
    });
}

/* MATCH HISTORY */
function getMatches() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please login first");
    return;
  }

  fetch(BASE_URL + "/match/my", {
    headers: {
      "Authorization": "Bearer " + token
    }
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("matches").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => {
      console.error(err);
      alert("Error loading matches");
    });
}
