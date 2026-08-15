// Renders the community analytics charts using Chart.js
document.addEventListener("DOMContentLoaded", () => {
    if (typeof CHART_DATA === "undefined" || typeof Chart === "undefined") return;

    const palette = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#0ea5e9", "#22c55e", "#f97316"];

    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.color = "#334155";

    function makeBarChart(canvasId, dataKey, label) {
        const el = document.getElementById(canvasId);
        const data = CHART_DATA[dataKey];
        if (!el || !data || !data.labels.length) return;
        new Chart(el, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [{
                    label,
                    data: data.values,
                    backgroundColor: palette,
                    borderRadius: 8,
                    maxBarThickness: 46,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: "#f1f5f9" } },
                    x: { grid: { display: false } },
                },
            },
        });
    }

    function makeDoughnutChart(canvasId, dataKey) {
        const el = document.getElementById(canvasId);
        const data = CHART_DATA[dataKey];
        if (!el || !data || !data.labels.length) return;
        new Chart(el, {
            type: "doughnut",
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: palette,
                    borderWidth: 2,
                    borderColor: "#ffffff",
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { position: "bottom", labels: { boxWidth: 12, padding: 14 } } },
            },
        });
    }

    makeBarChart("ageChart", "age", "Participants");
    makeDoughnutChart("occupationChart", "occupation");
    makeBarChart("investmentChart", "investment", "Participants");
    makeDoughnutChart("upiChart", "upi");
    makeBarChart("fraudChart", "fraud", "Participants");
    makeDoughnutChart("knowledgeChart", "knowledge");
});
