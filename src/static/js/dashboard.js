document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('url-input');
    const repeatInput = document.getElementById('repeat-input');
    const startButton = document.getElementById('start-button');
    const stopButton = document.getElementById('stop-button');
    const resultsContainer = document.getElementById('results-container');
    const alertContainer = document.getElementById('alert-container');
    let chart = null;
    let intervalId;

    // Make runBenchmark available globally
    window.runBenchmark = async function() {
        const urlInput = document.getElementById('urlInput').value;
        const repeatCount = parseInt(document.getElementById('repeatCount').value) || 3;
        
        // Show loading state
        document.getElementById('resultText').innerHTML = 'Running benchmark...';
        
        try {
            const response = await fetch('/benchmark', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: urlInput,
                    repeat: repeatCount
                })
            });

            const data = await response.json();
            
            if (data.error) {
                document.getElementById('resultText').innerHTML = `Error: ${data.error}`;
                return;
            }

            // Ensure data arrays exist before processing
            const http2Data = data['HTTP/2'] || [];
            const http3Data = data['HTTP/3'] || [];

            // Calculate averages safely
            const http2Avg = calculateAverage(http2Data);
            const http3Avg = calculateAverage(http3Data);

            // Update chart if it exists
            if (window.benchmarkChart) {
                window.benchmarkChart.data.datasets[0].data = [http2Avg, http3Avg];
                window.benchmarkChart.update();
            }

            // Display results
            document.getElementById('resultText').innerHTML = `
                <h3>Results:</h3>
                <p>HTTP/2: ${formatTime(http2Avg)} seconds</p>
                <p>HTTP/3: ${formatTime(http3Avg)} seconds</p>
                <p class="small">Individual request times:</p>
                <p class="small">HTTP/2: ${formatArray(http2Data)}</p>
                <p class="small">HTTP/3: ${formatArray(http3Data)}</p>
            `;
        } catch (error) {
            document.getElementById('resultText').innerHTML = `Error: ${error.message}`;
        }
    };

    function calculateAverage(times) {
        if (!Array.isArray(times) || times.length === 0) {
            return 0;
        }
        const validTimes = times.filter(time => time !== null && !isNaN(time));
        return validTimes.length ? validTimes.reduce((a, b) => a + b, 0) / validTimes.length : 0;
    }

    function initChart() {
        const ctx = document.getElementById('resultsChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['HTTP/1.1', 'HTTP/2'],
                datasets: [{
                    label: 'Response Time (seconds)',
                    data: [0, 0],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 99, 132, 0.5)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Response Time (seconds)'
                        }
                    }
                }
            }
        });
    }

    startButton.addEventListener('click', function() {
        const url = urlInput.value;
        const repeat = repeatInput.value;

        if (!url) {
            showAlert('Please enter a valid URL.', 'danger');
            return;
        }

        startBenchmark(url, repeat);
    });

    stopButton.addEventListener('click', function() {
        stopBenchmark();
    });

    function startBenchmark(url, repeat) {
        resultsContainer.innerHTML = '';
        const data = {
            url: url,
            repeat: repeat
        };

        fetch('/start-benchmark', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Benchmark started successfully!', 'success');
                startTracking();
            } else {
                showAlert('Error starting benchmark: ' + data.message, 'danger');
            }
        });
    }

    function stopBenchmark() {
        clearInterval(intervalId);
        fetch('/stop-benchmark', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('Benchmark stopped successfully!', 'success');
                } else {
                    showAlert('Error stopping benchmark: ' + data.message, 'danger');
                }
            });
    }

    function startTracking() {
        intervalId = setInterval(() => {
            fetch('/get-results')
                .then(response => response.json())
                .then(data => {
                    updateResults(data);
                    updateChart(data);
                });
        }, 2000);
    }

    function updateResults(data) {
        resultsContainer.innerHTML = '';
        data.results.forEach(result => {
            const div = document.createElement('div');
            div.textContent = `URL: ${result.url}, Time: ${result.time} sec`;
            resultsContainer.appendChild(div);
        });
    }

    function updateChart(data) {
        if (chart) {
            chart.data.datasets[0].data = [
                average(data['HTTP/1.1']),
                average(data['HTTP/2'])
            ];
            chart.update();
        } else {
            initChart();
        }
    }

    function showAlert(message, type) {
        alertContainer.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
        setTimeout(() => {
            alertContainer.innerHTML = '';
        }, 3000);
    }

    function average(arr) {
        const validTimes = arr.filter(time => time !== null);
        return validTimes.length ? validTimes.reduce((a, b) => a + b) / validTimes.length : 0;
    }

    function formatResults(times) {
        const validTimes = times.filter(time => time !== null);
        if (!validTimes.length) return 'No valid measurements';

        const avg = average(validTimes);
        return `Average: ${avg.toFixed(3)}s (${validTimes.length} successful requests)`;
    }

    function formatTime(time) {
        return typeof time === 'number' ? time.toFixed(3) : 'N/A';
    }

    function formatArray(arr) {
        if (!Array.isArray(arr)) return 'No data';
        return arr.map(t => typeof t === 'number' ? t.toFixed(3) : 'failed').join(', ');
    }

    // Initialize chart when page loads
    initChart();
});