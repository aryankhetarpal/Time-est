function calculate() {
    // Get form values
    const height = document.getElementById('height').value;
    const width = document.getElementById('width').value;
    const length = document.getElementById('length').value;
    const steelGrade = document.getElementById('steel_grade').value;
    const cutType = document.getElementById('cut_type').value;
    const finalDimension = document.getElementById('final_dimension').value;

    // Prepare data to send
    const data = {
        height: height,
        width: width,
        length: length,
        steel_grade: steelGrade,
        cut_type: cutType,
        final_dimension: finalDimension
    };

    // Send data to Flask server
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Display results
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = ''; // Clear previous results
        if (data.error) {
            resultsDiv.innerHTML = `<p>${data.error}</p>`;
        } else {
            data.forEach(item => {
                resultsDiv.innerHTML += `<p>Machine: ${item.machine_name}, Cutting Time: ${item.cutting_time} minutes</p>`;
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
