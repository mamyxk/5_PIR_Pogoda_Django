const SENSOR_LOGS_URI = "fetch_sensor_logs"
const SENSOR_NAMES_URI = "fetch_sensor_name"

let selectedValues = []
let charts = []

document.addEventListener('DOMContentLoaded', () => {
    const elems = document.querySelectorAll('select');
    const instances = M.FormSelect.init(elems);

    selectedValues = instances[0].getSelectedValues();

    document.querySelector('#sensors-select').addEventListener('change', () => {
        selectedValues = instances[0].getSelectedValues();

        refreshDisplay();
    })

    charts = initializeCharts();

});

setInterval(refreshDisplay, 1000)

function isDataValid(data) {
    return data.length !== 0 && data.every(item => !isNaN(item) && item !== '')
}

function refreshDisplay() {
    if (!isDataValid(selectedValues)) {
        updateReadings({
            temperature: 0,
            humidity: 0,
            pressure: 0,
            altitude: 0
        })
        updateCharts(charts, [])
        return;
    }
    fetch(SENSOR_LOGS_URI, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({ selectedSensors: selectedValues })
    })
        .then(res => res.json())    //code formatter robi mi tu wcięcie >:(
        .then(data => {
            updateReadings(getAverageReadingsFromAllSensors(data.context));
            updateCharts(charts, data.context);
        })
        .catch(err => {
            console.error(err)
        })
}

function getAverageReadingsFromAllSensors(data) {
    const result = Object.values(data).reduce((acc, sensor) => ({
        temperature: acc.temperature + sensor[0].temperature,
        humidity: acc.humidity + sensor[0].humidity,
        pressure: acc.pressure + sensor[0].pressure,
        altitude: acc.altitude + sensor[0].altitude
    }), {
        temperature: 0,
        humidity: 0,
        pressure: 0,
        altitude: 0
    })

    const sensorCount = Object.keys(data).length

    return {
        temperature: result.temperature / sensorCount,
        humidity: result.humidity / sensorCount,
        pressure: result.pressure / sensorCount,
        altitude: result.altitude / sensorCount
    }
}

function updateReadings(data) {
    document.querySelector('#temperature-field').innerText = `${data.temperature.toFixed(4)} °C`;
    document.querySelector('#humidity-field').innerText = `${data.humidity.toFixed(4)} %`;
    document.querySelector('#pressure-field').innerText = `${data.pressure.toFixed(4)} hPa`;
    document.querySelector('#altitude-field').innerText = `${data.altitude.toFixed(4)} m n.p.m.`;
}

function initializeCharts() {
    const temperatureChartCtx = document.querySelector('#temperature-chart');
    const humidityChartCtx = document.querySelector('#humidity-chart');
    const pressureChartCtx = document.querySelector('#pressure-chart');
    const altitudeChartCtx = document.querySelector('#altitude-chart');

    const temperatureChart = setupChart(temperatureChartCtx, 'temperature')
    const humidityChart = setupChart(humidityChartCtx, 'humidity')
    const pressureChart = setupChart(pressureChartCtx, 'pressure')
    const altitudeChart = setupChart(altitudeChartCtx, 'altitude')

    return [
        temperatureChart,
        humidityChart,
        pressureChart,
        altitudeChart
    ]
}

function updateCharts(charts, data) {
    console.log(charts)
    charts.forEach(async (chartWithName) => {
        const { name, chart } = chartWithName;
        const { timestamps, datasets } = await processSensorLogs(data, name);

        chart.data.labels = timestamps;
        chart.data.datasets = datasets;
        chart.update();
    })
}

// Gdzie są TYPY?! (ja chcę typescript .·´¯`(>▂<)´¯`·. )
// name musi być jednym z {temperature, humidity, pressure, altitude}
function setupChart(ctx, name) {
    return {
        name,
        chart: new Chart(ctx, {
            type: 'line',
            data: {},
            options: {
                scales: {
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: name.toUpperCase()
                    }
                },
                animation: {
                    duration: 0
                }
            }
        })
    }
}

async function processSensorLogs(data, parameterName) {
    let timestamps = []
    const datasets = []

    for (let sensorId in data) {
        timestamps = data[sensorId].map(reading => {
            datetime = new Date(reading.timestamp)
            return `${datetime.getHours().toFixed(2)}:${datetime.getMinutes().toFixed(2)}:${datetime.getSeconds().toFixed(2)}`
        });
        datasets.push({
            label: await getSensorName(sensorId),
            data: data[sensorId].map(reading => reading[parameterName])
        })
    }

    return {
        timestamps,
        datasets
    }

}

function getSensorName(sensorId) {
    return fetch(SENSOR_NAMES_URI, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({ sensor_id: sensorId })
    })
        .then(res => res.json())    //code formatter robi mi tu wcięcie >:(
        .then(data => data.sensor_name)
        .catch(err => {
            console.error(err)
        })
}