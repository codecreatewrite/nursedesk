document.getElementById("loginBtn").addEventListener("click", async () => {
  const username = document.getElementById("username").value;
  const password = document.getElementById("pwd").value;
  const messageDiv = document.getElementById("message");

  if (!username || !password) {
    messageDiv.textContent = "Please enter username and password.";
    return;
  }

  const response = await fetch("https://nursedesk.onrender.com/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `username=${username}&password=${password}`
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    messageDiv.style.color = "green";
    messageDiv.textContent = "Login successful. Redirecting...";
    window.location.href = "nursedesk.html";
  } else {
    messageDiv.style.color = "red";
    messageDiv.textContent = "Invalid username or password.";
  }
});
