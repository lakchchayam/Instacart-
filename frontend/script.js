document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    if (window.lucide) {
        window.lucide.createIcons();
    }

    // Chart.js Theme Defaults
    Chart.defaults.color = '#7f8c8d';
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.scale.grid.color = 'rgba(0, 0, 0, 0.05)';

    // 1. DYNAMICS CHART (Availability Trend)
    const ctxDynamics = document.getElementById('dynamicsChart').getContext('2d');

    const dynamicsLabels = ['12 AM', '4 AM', '8 AM', '12 PM', '4 PM', '8 PM', '11 PM'];

    new Chart(ctxDynamics, {
        type: 'line',
        data: {
            labels: dynamicsLabels,
            datasets: [
                {
                    label: 'Predicted Availability',
                    data: [0.98, 0.95, 0.88, 0.82, 0.75, 0.68, 0.72],
                    borderColor: '#24be51',
                    backgroundColor: 'rgba(36, 190, 81, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4,
                },
                {
                    label: 'Actual Shops',
                    data: [0.99, 0.96, 0.85, 0.80, 0.70, 0.65, 0.70],
                    borderColor: '#003366',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    min: 0.5,
                    max: 1.0,
                    ticks: { callback: value => (value * 100) + '%' }
                }
            }
        }
    });

    // 2. FORECAST CHART (Substitution Confidence)
    const ctxForecast = document.getElementById('forecastChart').getContext('2d');

    new Chart(ctxForecast, {
        type: 'bar',
        data: {
            labels: ['Brand Fit', 'Dietary Match', 'Price Delta', 'Availability'],
            datasets: [{
                label: 'Confidence Factor',
                data: [0.95, 0.98, 0.85, 0.92],
                backgroundColor: ['#24be51', '#24be51', '#24be51', '#003366'],
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: { max: 1.0, display: false }
            }
        }
    });

    // Modal Logic
    const modal = document.getElementById("aboutModal");
    const btn = document.getElementById("aboutBtn");
    const span = document.getElementsByClassName("close")[0];

    btn.onclick = () => modal.style.display = "block";
    span.onclick = () => modal.style.display = "none";
    window.onclick = (event) => {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Optimized Navbar Scroll
    const nav = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }, { passive: true });
});
