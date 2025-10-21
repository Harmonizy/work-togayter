// ====== ดึงสีตามธีม ======
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

// ====== โหลดกราฟ CAP จาก API ======
async function loadCharts() {
    const colors = getChartColorsArray("countries_charts");
    if (!colors) return;

    try {
        const response = await fetch("/safety-dashboard/apis/get-cap_data_api");
        if (!response.ok) throw new Error("❌ API โหลดข้อมูลไม่สำเร็จ");
        const capData = await response.json();

        // ✅ เตรียมข้อมูลจาก API
        const categories = capData.map(item => item["hazard_log__affiliation__short_name"] || "ไม่ทราบหน่วย");
        const seriesData = capData.map(item => item.total);

        // ✅ ตั้งค่า ApexCharts
        const chartOptions = {
            series: [{
                name: "จำนวน CAP",
                data: seriesData,
            }],
            chart: {
                type: "bar",
                height: 436,
                toolbar: { show: false }
            },
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
                style: {
                    fontSize: "12px",
                    fontWeight: 400,
                    colors: ["#adb5bd"]
                },
            },
            legend: { show: false },
            grid: { show: false },
            xaxis: { categories: categories },
        };

        // ✅ สร้างหรืออัปเดตกาฟ
        if (countriesChart) countriesChart.destroy();
        countriesChart = new ApexCharts(document.querySelector("#countries_charts"), chartOptions);
        countriesChart.render();

    } catch (err) {
        console.error("📉 โหลดกราฟ CAP ล้มเหลว:", err);
    }
}

// ====== โหลดตอนหน้าเสร็จหรือ resize ======
window.addEventListener("resize", () => setTimeout(loadCharts, 0));
window.addEventListener("DOMContentLoaded", loadCharts);
