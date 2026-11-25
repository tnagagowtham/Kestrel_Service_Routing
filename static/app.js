const form = document.getElementById("route-form");
const button = document.getElementById("submit-btn");
const result = document.getElementById("result");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.classList.add("hidden");
  errorBox.classList.add("hidden");
  button.disabled = true;
  button.textContent = "Analysing request...";

  const payload = Object.fromEntries(new FormData(form).entries());
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");

    document.getElementById("team-name").textContent = data.predicted_team;
    document.getElementById("team-scope").textContent = data.team_scope;
    document.getElementById("note").textContent = data.note;
    const list = document.getElementById("reasons");
    list.replaceChildren();
    data.reasons.forEach((reason) => {
      const item = document.createElement("li");
      item.textContent = reason;
      list.appendChild(item);
    });
    result.classList.remove("hidden");
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.classList.remove("hidden");
  } finally {
    button.disabled = false;
    button.textContent = "Predict service team";
  }
});
