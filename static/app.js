function calculateCuttingTime() {
    const height = document.getElementById("height").value;
    const width = document.getElementById("width").value;
    const length = document.getElementById("length").value;
    const steelGrade = document.getElementById("grade").value;
    const cutType = document.getElementById("cut-type").value;
    const finalDimension = document.getElementById("final-dimension").value;

    const requestData = {
        height: height,
        width: width,
        length: length,
        steel_grade: steelGrade,
        cut_type: cutType,
        final_dimension: finalDimension
    };

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "";
        data.forEach(result => {
            resultsDiv.innerHTML += `Machine: ${result.machine_name}, Cutting Time: ${result.cutting_time} minutes<br>`;
        });
    })
    .catch(error => console.error('Error:', error));
}
