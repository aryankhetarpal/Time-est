function calculateCuttingTime() {
    const height = document.getElementById("height").value;
    const width = document.getElementById("width").value;
    const length = document.getElementById("length").value;
    const steelGrade = document.getElementById("steel_grade").value;
    const cutType = document.getElementById("cut_type").value;
    const finalDimension = document.getElementById("final_dimension").value;
    const numCuts = document.getElementById("num_cuts").value;

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

        if (data.length === 0) {
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
                    </tr>
                </thead>
                <tbody>
        `;

        data.forEach(result => {
            table += `
                <tr>
                    <td>${result.machine_name}</td>
                    <td>${Number(result.cutting_time).toFixed(2)}</td>
                    <td>${Number(result.sq_inches).toFixed(2)}</td>
                </tr>
            `;
        });

        table += "</tbody></table>";
        resultsDiv.innerHTML = table;
    })
    .catch(error => console.error('Error:', error));
}
