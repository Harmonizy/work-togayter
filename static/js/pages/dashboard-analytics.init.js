// ====================================
//   ดึงสีตามธีม
// ====================================
function getChartColorsArray(chartId) {
    const el = document.getElementById(chartId);
    if (!el) return null;

    let colors = JSON.parse(el.getAttribute("data-colors"));
    return colors.map(color =>
        getComputedStyle(document.documentElement).getPropertyValue(color) || color
    );
}

// กราฟตัวแปร
let countriesChart = null;


// ====================================
//   สร้างกราฟจาก Django (ไม่ใช้ API แล้ว)
// ====================================
function loadCharts() {

    const el = document.getElementById("countries_charts");
    if (!el) return;

    const colors = getChartColorsArray("countries_charts");

    // ดึง JSON จาก Django
    const capData = JSON.parse(el.dataset.cap);

    // เตรียมข้อมูล
    const categories = capData.map(i =>
        i["hazard_log__affiliation__short_name"] || "ไม่ทราบหน่วย"
    );
    const planning = capData.map(i => i.planning);
    const in_progress = capData.map(i => i.in_progress);
    const complete = capData.map(i => i.complete);

    const dynamicHeight = Math.max(436, categories.length * 28);

    const options = {
        series: [
            { name: "วางแผน", data: planning },
            { name: "กำลังดำเนินการ", data: in_progress },
            { name: "เสร็จสิ้น", data: complete }
        ],
        chart: {
            type: "bar",
            height: dynamicHeight,
            stacked: true,
            toolbar: { show: false }
        },
        plotOptions: {
            bar: { horizontal: true, borderRadius: 4 }
        },
        colors: ["#4babffff", "#f1c40f", "#28a745"],
        xaxis: { categories },
        legend: { position: "top" }
    };

    if (countriesChart) countriesChart.destroy();
    countriesChart = new ApexCharts(el, options);
    countriesChart.render();
}

// โหลดเมื่อพร้อม
document.addEventListener("DOMContentLoaded", loadCharts);
window.addEventListener("resize", () => setTimeout(loadCharts, 0));
