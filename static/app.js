function calculate() {
    const height = document.getElementById('height').value;
    const width = document.getElementById('width').value;
    const length = document.getElementById('length').value;
    const steel_grade = document.getElementById('steel_grade').value;
    const cut_type = document.getElementById('cut_type').value;
    const final_dimension = document.getElementById('final_dimension').value;

    const data = {
        height: height,
        width: width,
        length: length,
        steel_grade: steel_grade,
        cut_type: cut_type,
        final_dimension: final_dimension
    };

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        result.forEach(machine => {
            resultsDiv.innerHTML += `<p>Machine: ${machine.machine_name}, Cutting Time: ${machine.cutting_time} minutes</p>`;
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
