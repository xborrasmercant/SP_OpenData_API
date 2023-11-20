function getBarrios(distrito) {
    var dropdownBarrios = document.getElementById("barrioSelectorTagID");
    dropdownBarrios.innerHTML = "";

    fetch(`/api/barrios/${distrito}`)
        .then(response => response.json())
        .then(data => {
            data.barrioDict.forEach(barrio => {
                var barrioOption = document.createElement("option");
                barrioOption.value = barrio;
                barrioOption.text = barrio;
                dropdownBarrios.add(barrioOption);
            });
            dropdownBarrios.disabled = false;
        });
}


function getBarrioInfo(event) {
    event.preventDefault();

    var distrito = document.getElementById('distritoSelectorTagID').value;
    var barrio = document.getElementById('barrioSelectorTagID').value;
    var infoTable = document.getElementById('infoTable');

    fetch(`/api/neighborhoodData/${distrito}/${barrio}`)
        .then(response => response.json())
        .then(data => {
            var tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';

            var row = `<tr>
                        <td>${data.pobTotal}</td>
                        <td>${data.hTotal}</td>
                        <td>${data.mTotal}</td>
                    </tr>`;
            tableBody.innerHTML = row; // Add new row
            infoTable.style.display = "table"
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle errors, maybe display a message to the user
        });
}

function getBarrioPercentages(event) {
    event.preventDefault(); // Prevent the default form submission

    var distrito = document.getElementById('distritoSelectorTagID').value;
    var barrio = document.getElementById('barrioSelectorTagID').value;
    var infoTable = document.getElementById('infoTable');

    fetch(`/api/neighborhoodData/${distrito}/${barrio}`)
        .then(response => response.json())
        .then(data => {
            var tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';

            // Calculate percentages
            var hPercentage = (data.hTotal / data.pobTotal) * 100;
            var mPercentage = (data.mTotal / data.pobTotal) * 100;

            var row = `<tr>
                        <td>${hPercentage.toFixed(2)}%</td>
                        <td>${mPercentage.toFixed(2)}%</td>
                    </tr>`;
            tableBody.innerHTML = row; // Add new row
            infoTable.style.display = "table"
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // Handle errors, maybe display a message to the user
        });
}


async function compareBarrios(distrito, barrio1, barrio2) {
    try {
        const response = await fetch(`/api/compareBarrios/${distrito}/${barrio1}/${barrio2}`);
        const data = await response.json();
        // Process and display the comparison data
        // For example, update the DOM with the comparison result
    } catch (error) {
        console.error('Error:', error);
    }
}
