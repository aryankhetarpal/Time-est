document.getElementById("height").addEventListener("input", function() {
    const heightValue = this.value.trim().toLowerCase();
    const cutTypeSelect = document.getElementById("cut-type");

    if (heightValue === "dia") {
        cutTypeSelect.value = "dia";
        cutTypeSelect.disabled = true; // prevent changing cut type manually
    } else {
        cutTypeSelect.disabled = false;
    }
});

function calculateCuttingTime() {
    const height = document.getElementById("height").value;
    const width = Number(document.getElementById("width").value);
    const length = Number(document.getElementById("length").value);
    const steelGrade = document.getElementById("grade").value;
    const cutType = document.getElementById("cut-type").value;
    const finalDimension = Number(document.getElementById("final-dimension").value);
    const numCuts = Number(document.getElementById("num-cuts").value);

    const requestData = {
        height: height,
        width: width,
        length: length,
        steel_grade: steelGrade,
        cut_type: cutType,
        final_dimension: finalDimension,
        num_cuts: numCuts
    };

    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";

        if (!data || data.length === 0) {
            resultsDiv.innerHTML = "<p>No suitable machines found.</p>";
            return;
        }

        // Build table
        let table = `
            <table border="1" cellpadding="6" cellspacing="0">
                <thead>
                    <tr>
                        <th>Machine</th>
                        <th>Cutting Time (min)</th>
                        <th>Sq Inches (Total for ${numCuts} cut${numCuts > 1 ? 's' : ''})</th>
                        <th>Can Cut?</th>
                    </tr>
                </thead>
                <tbody>
        `;

        data.forEach(result => {
            table += `
                <tr style="background-color:${result.can_cut ? '#e6ffe6' : '#ffe6e6'}">
                    <td>${result.machine_name}</td>
                    <td>${Number(result.cutting_time).toFixed(2)}</td>
                    <td>${Number(result.sq_inches).toFixed(2)}</td>
                    <td>${result.can_cut ? "✅ Yes" : "❌ No"}</td>
                </tr>
            `;
        });

        table += "</tbody></table>";
        resultsDiv.innerHTML = table;
    })
    .catch(error => console.error('Error:', error));
}
