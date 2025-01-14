const ctx = document.getElementById('attendanceChart').getContext('2d');
// const data = {{ statuses | tojson }};
// 上記コードはflask外部ファイルとして記述できないらしい
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [...Array(24).keys()].map(hour => `${hour}:00 - ${hour + 1}:00`),
        datasets: [{
            label: 'Presence Time (minutes)',
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        // <!--indexAxis: 'y',--> // 横棒グラフ コメントアウト中
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Hours'
                }
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Presence Time (minutes)'
                }
            }
        }
    }
});