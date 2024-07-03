function drawCateStats (labels, data) {
    const ctx = document.getElementById('cateStats');
//    const rndNum = () => Math.floor(Math.random() * 254 + 1);
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Số lượng sách trong từng thể loại',
                data: data,
                borderWidth: 1,
                backgroundColor: ['red', 'blue', 'green','rgba(250, 200, 50, 0.8)']
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function drawRevenueStats (labels, data) {
    const ctx = document.getElementById('revenueStats');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Doanh thu theo tháng',
                data: data,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function drawFrequencyStats (labels, data) {
    const ctx = document.getElementById('frequencyStats');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tần suất sách bán',
                data: data,
                borderWidth: 1,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}