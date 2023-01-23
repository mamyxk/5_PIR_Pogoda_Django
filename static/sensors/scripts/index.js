const URL = "fetch_sensor_logs?"

let selectedValues = []

document.addEventListener('DOMContentLoaded', () => {
    const elems = document.querySelectorAll('select');
    const instances = M.FormSelect.init(elems);
    
    selectedValues = instances[0].getSelectedValues();

    document.querySelector('#sensors-select').addEventListener('change', () => {
        selectedValues = instances[0].getSelectedValues();

        refreshDisplay()
    })

});

setInterval(refreshDisplay, 1000)

function refreshDisplay() {
    console.log(selectedValues)
    if (selectedValues.length === 0) {
        updateReadings({
            temperature: 0,
            humidity: 0,
            pressure: 0,
            altitude: 0
        })
        return;
    }
    fetch(URL + new URLSearchParams({
        selectedSensors: selectedValues.join()
    }), {
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
        .then(res => res.json())    //code formatter robi mi tu wcięcie >:(
        .then(data => {
            console.log(data.context)
            updateReadings(data.context[0])
        })
        .catch(err => {
            console.error(err)
        })
}

function updateReadings(data) {
    document.querySelector('#temperature-field').innerText = `${data.temperature.toFixed(4)} °C`
    document.querySelector('#humidity-field').innerText = `${data.humidity.toFixed(4)} %`
    document.querySelector('#pressure-field').innerText = `${data.pressure.toFixed(4)} hPa`
    document.querySelector('#altitude-field').innerText = `${data.altitude.toFixed(4)} m n.p.m.`
}