const ctx = document.getElementById('performanceChart').getContext('2d');

const performanceChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['HTTP/1.1', 'HTTP/2'],
        datasets: [{
            label: 'Average Response Time (s)',
            data: [], // This will be populated dynamically
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Time (seconds)'
                }
            }
        },
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.dataset.label + ': ' + tooltipItem.raw + ' seconds';
                    }
                }
            }
        }
    }
});

// Function to update the chart with new data
function updateChart(http1Time, http2Time) {
    performanceChart.data.datasets[0].data = [http1Time, http2Time];
    performanceChart.update();
}