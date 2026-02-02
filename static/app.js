function toggleHeightInput() {
  const cutType = document.getElementById("cut-type").value;
  const heightInput = document.getElementById("height");
  const finalDimInput = document.getElementById("final-dimension");

  if (cutType === "dia") {
    heightInput.value = "Dia";
    heightInput.disabled = true;
    finalDimInput.disabled = true;
  } else {
    heightInput.disabled = false;
    finalDimInput.disabled = false;

    if (heightInput.value.toLowerCase() === "dia") {
      heightInput.value = "";
    }
  }
}

async function calculateCuttingTime() {
  const payload = {
    height: document.getElementById("height").value,
    width: document.getElementById("width").value,
    length: document.getElementById("length").value,
    steel_grade: document.getElementById("grade").value,
    cut_type: document.getElementById("cut-type").value,
    final_dimension: document.getElementById("final-dimension").value,
    num_cuts: document.getElementById("num-cuts").value
  };

  const response = await fetch("/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const results = await response.json();

  const table = document.getElementById("results-table");
  const tbody = table.querySelector("tbody");
  tbody.innerHTML = "";

  results.forEach(machine => {
    const row = document.createElement("tr");

    if (!machine.can_cut) row.classList.add("unfit");
    if (machine.machine_name === "BITL") row.classList.add("bitl");

    row.innerHTML = `
      <td>${machine.machine_name}</td>
      <td>${Number(machine.cutting_time).toFixed(2)}</td>
      <td>${Number(machine.sq_inches).toFixed(2)}</td>
      <td>${machine.can_cut ? "✅ Yes" : "❌ No"}</td>
    `;

    tbody.appendChild(row);
  });

  table.style.display = "table";
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", toggleHeightInput);
