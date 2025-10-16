function getChartColorsArray(chartId) {
    const el = document.getElementById(chartId);
    if (!el) return null;

    const theme = document.documentElement.getAttribute("data-theme") || "";
    const attr = theme ? `data-colors-${theme}` : "data-colors";

    let colors = el.getAttribute(attr) || el.getAttribute("data-colors");
    if (!colors) {
        console.warn("⚠️ data-colors attribute not found on", chartId);
        return null;
    }

    colors = JSON.parse(colors);
    return colors.map(function (value) {
        const clean = value.replace(" ", "");
        if (clean.indexOf(",") === -1) {
            return getComputedStyle(document.documentElement).getPropertyValue(clean) || clean;
        } else {
            const parts = clean.split(",");
            if (parts.length === 2) {
                return `rgba(${getComputedStyle(document.documentElement).getPropertyValue(parts[0])},${parts[1]})`;
            }
            return clean;
        }
    });
}

let countriesChart = null;
let audiencesMetricsCharts = null;
let audiencesSessionsCountryChart = null;
let userDevicePieCharts = null;

function loadCharts() {
    // ===== COUNTRIES CHART =====
    const colors = getChartColorsArray("countries_charts");
    if (colors) {
        const chartOptions = {
            series: [{
                name: "Reports",
                data: [
                    120, 85, 95, 200, 150, 130, 175, 90, 110, 160,
                    140, 125, 100, 80, 95, 70                      
                ],
            }],
            chart: { type: "bar", height: 436, toolbar: { show: false } },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    horizontal: true,
                    distributed: true,
                    dataLabels: { position: "top" },
                },
            },
            colors: colors,
            dataLabels: {
                enabled: true,
                offsetX: 32,
                style: { fontSize: "12px", fontWeight: 400, colors: ["#adb5bd"] },
            },
            legend: { show: false },
            grid: { show: false },
            xaxis: {
                categories: [
                    "กองบิน 1", "กองบิน 2", "กองบิน 3", "กองบิน 4", "กองบิน 5",
                    "กองบิน 6", "กองบิน 7", "กองบิน 21", "กองบิน 23", "กองบิน 41",
                    "กองบิน 46", "กองบิน 56", "รร.การบิน", "คปอ.", "อย.", "ศปอว.ทอ."
                ],
            },
        };

        if (countriesChart) countriesChart.destroy();
        countriesChart = new ApexCharts(document.querySelector("#countries_charts"), chartOptions);
        countriesChart.render();
    }

    // ===== ตัวอื่น (ถ้ามีอยู่แล้วใน template เดิม) =====
    // คุณสามารถเรียก chart อื่นๆ ต่อได้ เช่น audiences_metrics_charts, user_device_pie_charts ฯลฯ
}

// โหลดตอนหน้าเสร็จ
window.addEventListener("resize", () => setTimeout(loadCharts, 0));
window.addEventListener("DOMContentLoaded", loadCharts);
